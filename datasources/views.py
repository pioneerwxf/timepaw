from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from timepaw.profiles.models import Profile
from timepaw.datasources.models import DataSource
from timepaw.paws.models import Paw, Img
from timepaw.paws.views import sync_source
from timepaw.utils.consts import *
from timepaw.datasources.top import OpenTaobao
from datetime import datetime,date,time
from json import JSONDecoder, JSONEncoder
from urllib import unquote
import oauth2 as oauth
import urlparse
import urllib2, urllib
import feedparser
import hashlib
import hmac
import time
import random
import md5
import base64

# DataSource Manage & Delete functions

def manage(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        profile = Profile.objects.get(pk = uid)
        email_md5 = hashlib.md5()
        email_md5.update(profile.email)
        return render_to_response('datasources/services.html', {'gravatar': email_md5.hexdigest(), 'datasources':profile.datasource_set.all()}, context_instance=RequestContext(request))
    else:
        return redirect('/login')

def delete(request, did):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        d = DataSource.objects.get(pk = did)
        if d in p.datasource_set.all():
            d.delete()
            return redirect('/datasources')
        else:
            return redirect('/login')
    else:
        return redirect('/login')

# Sina Weibo connect function

def weibo_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        red_url = "https://api.weibo.com/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s" % (WEIBO_KEY, BASE_URL+"/datasources/weibo_callback")
        return redirect(red_url)
    else:
        return redirect('/login')
        
def weibo_callback(request):
    
    code = request.GET['code']
    token_url = "https://api.weibo.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s" % (WEIBO_KEY, WEIBO_SECRET, BASE_URL+"/datasources/weibo_callback", code)
    info = JSONDecoder().decode(urllib2.urlopen(token_url, "").read())
    
    uid = request.session.get('uid', default = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        uid_url = "https://api.weibo.com/2/account/get_uid.json?access_token=%s" % (info['access_token'])
        uid = JSONDecoder().decode(urllib2.urlopen(uid_url).read())['uid']
        info['uid'] = uid
        uinfo_url = "https://api.weibo.com/2/users/show.json?access_token=%s&uid=%s" % (info['access_token'], uid)
        user_info = JSONDecoder().decode(urllib2.urlopen(uinfo_url).read())
        en_info = JSONEncoder().encode(info)
        d = DataSource.objects.create(source_name="weibo", auth_info=en_info, account_name=user_info['screen_name'], owner=p)
        sync_source(d)
        return redirect('/datasources')

# Douban connect function

def douban_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        request_token_url = 'http://www.douban.com/service/auth/request_token'
        authorize_url = 'http://www.douban.com/service/auth/authorize'

        consumer = oauth.Consumer(DOUBAN_KEY, DOUBAN_SECRET)
        client = oauth.Client(consumer)
        
        resp, content = client.request(request_token_url, "GET")
        
        request_token = dict(urlparse.parse_qsl(content))
        request.session['rt_ot'] = request_token['oauth_token']
        request.session['rt_ots'] = request_token['oauth_token_secret']
        
        red_url = "%s?oauth_token=%s&oauth_callback=%s" % (authorize_url, request_token['oauth_token'], BASE_URL+"/datasources/douban_callback")
        return redirect(red_url)
    else:
        return redirect('/login')

def douban_callback(request):
    
    oauth_verifier = request.GET['oauth_token']
    access_token_url = 'http://www.douban.com/service/auth/access_token'
    
    consumer = oauth.Consumer(DOUBAN_KEY, DOUBAN_SECRET)
    token = oauth.Token(request.session['rt_ot'], request.session['rt_ots'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    
    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    
    uid = request.session.get('uid', default = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        
        token = oauth.Token(key=access_token['oauth_token'], secret=access_token['oauth_token_secret'])
        client = oauth.Client(consumer, token)
        
        url = "http://api.douban.com/people/%s?alt=json" % (access_token['douban_user_id'])
        resp, content = client.request(url, "GET")
        user_info = JSONDecoder().decode(content)
        
        en_info = JSONEncoder().encode(access_token)
        d = DataSource.objects.create(source_name="douban", auth_info=en_info, account_name=user_info['title']['$t'], owner=p)
        sync_source(d)
        return redirect('/datasources')
    else:
        return redirect('/login')

# Renren connect function

def renren_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:        
        authorize_url = 'https://graph.renren.com/oauth/authorize'
        
        red_url = "%s?client_id=%s&response_type=code&redirect_uri=%s&scope=read_user_blog read_user_photo read_user_status read_user_album" % (authorize_url, RENREN_KEY, BASE_URL+"/datasources/renren_callback")
        return redirect(red_url)
    else:
        return redirect('/login')

def renren_callback(request):
    code = request.GET['code']
    token_url = "https://graph.renren.com/oauth/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s" % (code, RENREN_KEY, RENREN_SECRET, BASE_URL+"/datasources/renren_callback")
    
    info = JSONDecoder().decode(urllib2.urlopen(token_url).read())
    info['albums'] = {}
    account_name = info['user']['name']
    uid = request.session.get('uid', default = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        
        en_info = JSONEncoder().encode(info)
        d = DataSource.objects.create(source_name="renren", auth_info=en_info, account_name = account_name, owner=p)
        sync_source(d)
        return redirect('/datasources')
    else:
        return redirect('/login')

# RSS connect function

def rss_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        if request.method == 'POST':
            p = Profile.objects.get(pk = uid)
            info = {}
            info['url'] = request.POST['url']
            f = feedparser.parse(info['url'])
            feed_title = f.feed.title
            en_info = JSONEncoder().encode(info)
            d = DataSource.objects.create(source_name="rss", auth_info=en_info, account_name=feed_title, owner=p)
            sync_source(d)
            return redirect('/datasources')
        else:
            return render_to_response('datasources/rss_add.html', {}, context_instance=RequestContext(request))
    else:
        return redirect('/login')

# GitHub connect function

def github_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        auth_url = "https://github.com/login/oauth/authorize?client_id=%s&redirect_uri=%s" % (GITHUB_KEY, BASE_URL+'/datasources/github_callback')
        return redirect(auth_url)
    else:
        return redirect('/login')

def github_callback(request):
    code = request.GET['code']
    uid = request.session.get('uid', defautl = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        token_url = "https://github.com/login/oauth/access_token?client_id=%s&client_secret=%s&code=%s" % (GITHUB_KEY, GITHUB_SECRET, code)
        info = JSONDecoder().decode(urllib2.urlopen(token_url, "").read())
        uinfo_url = "https://api.github.com/user?access_token=%s" % (info['access_token'])
        uinfo = JSONDecoder().decode(urllib2.urlopen(uinfo_url).read())
        info['id'] = uinfo['id']
        account_name = uinfo['name']
        d = DataSource.objects.create(source_name = "github", auth_info = JSONEncoder().encode(info), account_name = account_name, owner = p)
        sync_source(d)
        return redirect('/datasources')
    else:
        return redirect('/login')

# QQ connect function


def tqq_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        request_token_url = 'https://open.t.qq.com/cgi-bin/request_token?'
        authorize_url = 'https://open.t.qq.com/cgi-bin/authorize'
        
        consumer = oauth.Consumer(QQ_KEY, QQ_SECRET)
        client = oauth.Client(consumer)
        body = urllib.urlencode(dict(oauth_callback=BASE_URL+"/datasources/tqq_callback"))
        resp, content = client.request(request_token_url, "POST", body=body)
        request_token = dict(urlparse.parse_qsl(content))
        request.session['rt_ot'] = request_token['oauth_token']
        request.session['rt_ots'] = request_token['oauth_token_secret']
        
        red_url = "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
        return redirect(red_url)
    else:
        return redirect('/login')

def tqq_callback(request):
    oauth_verifier = request.GET['oauth_verifier']
    access_token_url = 'https://open.t.qq.com/cgi-bin/access_token'
    
    consumer = oauth.Consumer(QQ_KEY, QQ_SECRET)
    token = oauth.Token(request.session['rt_ot'], request.session['rt_ots'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    
    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    
    uid = request.session.get('uid', default = None)
    if uid is not None:
        p = Profile.objects.get(pk = uid)
        
        token = oauth.Token(key=access_token['oauth_token'], secret=access_token['oauth_token_secret'])
        client = oauth.Client(consumer, token)
        
        url = "http://open.t.qq.com/api/user/info?format=json"
        resp, content = client.request(url, "GET")
        user_info = JSONDecoder().decode(content)
        
        en_info = JSONEncoder().encode(access_token)
        d = DataSource.objects.create(source_name="tqq", auth_info=en_info, account_name=user_info['data']['name'], owner=p)
        sync_source(d)
        return redirect('/datasources')
    else:
        return redirect('/login')
        

# Taobao.com connect function

def taobao_add(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        red_url = "http://container.open.taobao.com/container?appkey=%s&encode=utf-8" % (TAOBAO_KEY)
        return redirect(red_url)
    else:
        return redirect('/login')

def taobao_callback(request):
    top_appkey = request.GET['top_appkey']
    top_sign = request.GET["top_sign"]
    top_parameters = request.GET['top_parameters']
    top_session = request.GET['top_session'] #get 1
    top_secret = TAOBAO_SECRET
    
    # validate the signature
    m = md5.new()
    m.update(top_appkey)
    m.update(top_parameters)
    m.update(top_session)
    m.update(top_secret)
    base64str = base64.b64encode(m.digest())
    if cmp(base64str, top_sign)==0:    
        dec_parameters = base64.decodestring(unquote(top_parameters))
        array_parameters = dec_parameters.split('&')
        refresh_token = array_parameters[3].split('=')[1] #get2
        
        
        sign_str = "appkey"+TAOBAO_KEY+"refresh_token"+refresh_token+"sessionkey"+top_session+TAOBAO_SECRET
        hash = md5.new()
        hash.update(sign_str)
        sign = hash.hexdigest().upper()
        access_token_url = 'http://container.open.taobao.com/container/refresh?appkey=%s&refresh_token=%s&sessionkey=%s&sign=%s' \
                           % (TAOBAO_KEY, refresh_token, top_session, sign)
        info = JSONDecoder().decode(urllib2.urlopen(access_token_url, "").read())
        
     
        uid = request.session.get('uid', default = None)
        if uid is not None:
            p = Profile.objects.get(pk = uid)
            params = {
                        'method':'taobao.user.get',
                        'session':info['top_session'],
                        'fields':'nick',
                        'partner_id':'top-apitools',
                        'format':'json'
                    }

            op = OpenTaobao(TAOBAO_KEY,TAOBAO_SECRET)
            user_info = JSONDecoder().decode(op.get_result(params))
            en_info = JSONEncoder().encode(info)
            d = DataSource.objects.create(source_name="taobao", auth_info=en_info, account_name=user_info['user_get_response']['user']['nick'], owner=p)
            
            sync_source(d)
            return redirect('/datasources')
        else:
            return redirect('/login')
    else:
        red_url = "http://container.open.taobao.com/container?appkey=%s&encode=utf-8" % (TAOBAO_KEY)
        return redirect(red_url)
    