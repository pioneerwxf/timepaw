from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from timepaw.profiles.models import Profile
from timepaw.datasources.models import DataSource
from timepaw.paws.models import Paw, Img
from timepaw.paws import tasks
from timepaw.utils.consts import *
from json import JSONDecoder, JSONEncoder
from datetime import datetime, date
from time import mktime
from random import choice
import urlparse
import urllib2
import oauth2 as oauth
import hashlib
import feedparser

def get_all_date(profile):
    dates = []
    
    for d in profile.datasource_set.all():
        for p in d.paw_set.all():
            if p.type == u"renren album":
                for pic in p.img_set.all():
                    if not pic.upload_time.date() in dates:
                        dates.append(pic.upload_time.date())
            else:
                if not p.create_time.date() in dates:
                    dates.append(p.create_time.date())
    dates.sort()
    return dates

def get_related_dates(dates, date):
    ret = {}
    
    if (dates[0] == date):
        ret['prev'] = None
    else:
        ret['prev'] = dates[dates.index(date)-1].strftime("%Y%m%d")
    
    if (dates[-1] == date):
        ret['next'] = None
    else:
        ret['next'] = dates[dates.index(date)+1].strftime("%Y%m%d")
    
    return ret

def home(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        profile = Profile.objects.get(pk = uid)
        dates = get_all_date(profile)
        
        if dates:
            start_date = int(mktime(dates[0].timetuple()))
            end_date = int(mktime(dates[-1].timetuple()))
        else:
            start_date = int(mktime(datetime.now().date().timetuple()))
            end_date = start_date
        
        all_paws = []
        
        for d in profile.datasource_set.all():
            for p in d.paw_set.all():
                if p.type==u"renren album":
                    imgs = p.img_set.all()
                    if imgs:
                        day = imgs[0].upload_time.date()
                        # make a fake paw for each day's album update
                        tmp_p = Paw(source=p.source, type=p.type, title=p.title, create_time=imgs[0].upload_time)
                        tmp_p.images = []
                        for i in imgs:
                            if (i.upload_time.date() == day):
                                tmp_p.images.append(i)
                            else:
                                all_paws.append(tmp_p)
                                day = i.upload_time.date()
                                tmp_p = Paw(source=p.source, type=p.type, title=p.title, create_time=i.upload_time)
                                tmp_p.images = [i]
                        all_paws.append(tmp_p)
                else:
                    p.images = []
                    for i in p.img_set.all():
                        p.images.append(i)
                    all_paws.append(p)
        
        all_paws.sort(key = lambda p: p.create_time)
        
        dict_paws = []
        day_paws = []
        if (all_paws != []):
            day = all_paws[0].create_time.date()
            for p in all_paws:
                if (p.create_time.date() == day):
                    day_paws.append(p)
                else:
                    dict_paws.append(day_paws)
                    day = p.create_time.date()
                    day_paws = [p]
        dict_paws.append(day_paws)
        return render_to_response('paws/home.html', {'profile': profile, 'dict_paws': dict_paws, 'gravatar': calc_md5(profile.email), 'start_date' : start_date, 'end_date' : end_date}, context_instance=RequestContext(request))
    else:
        return redirect('/login')

def dairy(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        profile = Profile.objects.get(pk = uid)
        
        dates = get_all_date(profile)
        
        # get a random date of the memo;
        if request.GET.has_key('date') and (len(request.GET['date']) == 8):
            year = request.GET['date'][:4]
            month = request.GET['date'][4:6]
            day = request.GET['date'][-2:]
            memo_day = date(int(year), int(month), int(day))
        else:
            memo_day = choice(dates)
        
        related_dates = get_related_dates(dates, memo_day)
        
        all_paws = []
        
        fake_id = 1
        for d in profile.datasource_set.all():
            for p in d.paw_set.filter(create_time__contains = memo_day):
                if (p.type != u"renren album"):
                    p.images = []
                    for i in p.img_set.all():
                        p.images.append(i)
                    all_paws.append(p)
            for p in d.paw_set.filter(type = u"renren album"):
                imgs = p.img_set.filter(upload_time__contains = memo_day)
                if imgs:
                    # make a fake paw for memo day's album update
                    tmp_p = Paw(id = fake_id, source=p.source, type=p.type, title=p.title, create_time=imgs[0].upload_time)
                    tmp_p.images = imgs
                    all_paws.append(tmp_p)
                    fake_id += 1
        
        all_paws.sort(key = lambda p: p.create_time)
        
        return render_to_response('paws/dairy.html', {'profile': profile, 'all_paws': all_paws, 'prev_date': related_dates['prev'], 'next_date': related_dates['next'], 'current_day' : memo_day,'gravatar': calc_md5(profile.email)}, context_instance=RequestContext(request))
    else:
        return redirect('/login')

def sync_source(d):
    if d.source_name == "weibo":
        
        tasks.sync_weibo.apply_async(args = [d.id, 1, None], countdown = 1)
        
    elif d.source_name == "rss":
        
        tasks.sync_rss.apply_async(args = [d.id], countdown = 1)
        
    elif d.source_name == "douban":
        
        tasks.sync_douban_notes.apply_async(args = [d.id, 1, None], countdown = 1)
        
    elif d.source_name == "renren":
        
        tasks.sync_renren_blogs.apply_async(args = [d.id, 1, None], countdown = 1)
    
    elif d.source_name == "tqq":
        
        tasks.sync_tqq.apply_async(args=[d.id, 0, 0, 0, None], countdown = 1)
    
    elif d.source_name == "taobao":
        
        tasks.sync_taobao.apply_async(args=[d.id,1, None], countdown = 1)
        
    return

def sync(request, did):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        d = DataSource.objects.get(pk=did)
        sync_source(d)
        return redirect('/datasources')
    else:
        return redirect('/login')