# coding: utf-8
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from timepaw.profiles.models import Profile
from timepaw.paws.models import Paw, Img
from timepaw.datasources.models import DataSource
from timepaw.datasources.top import OpenTaobao
from timepaw.utils.consts import *
from json import JSONDecoder, JSONEncoder
from celery.task import task
from datetime import datetime
import urllib2
import urlparse
import oauth2 as oauth
import feedparser
import md5
import base64
import hashlib

# Sina Weibo sync task

@task(ignore_result=True)
def sync_weibo(did, page, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    url = "https://api.weibo.com/2/statuses/user_timeline.json?access_token=%s&uid=%s&page=%s&count=200" % (info['access_token'], info['uid'], page)
    statuses_info = JSONDecoder().decode(urllib2.urlopen(url).read())
    
    if statuses_info['statuses']:
        if (page == 1):
            new_latest = statuses_info['statuses'][0]['id']
        for status in statuses_info['statuses']:
            if (info.has_key('latest') and (status['id'] == info['latest'])):
                info['latest'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_weibo.apply_async(args = [did, 1, None], countdown = 84600)
                break
            new_paw = Paw.objects.create(source=d, type="weibo", content=status['text'], create_time=datetime.strptime(status['created_at'][0:20]+status['created_at'][-4:], "%a %b %d %H:%M:%S %Y"))
            if status.has_key('original_pic'):
                new_img = Img(album = new_paw, upload_time=new_paw.create_time)
                origin_tmp = NamedTemporaryFile(delete=True)
                origin_tmp.write(urllib2.urlopen(status['original_pic']).read())
                origin_tmp.flush()
                new_img.original.save(origin_tmp.name.split('/')[-1]+'.jpg', File(origin_tmp), save=False)
                thumb_tmp = NamedTemporaryFile(delete=True)
                thumb_tmp.write(urllib2.urlopen(status['thumbnail_pic']).read())
                thumb_tmp.flush()
                new_img.thumbnail.save(thumb_tmp.name.split('/')[-1]+'.jpg', File(thumb_tmp), save=True)
        if not (info.has_key('latest') and (status['id'] == info['latest'])):
            sync_weibo.apply_async(args = [did, page+1, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest'] = new_latest
        d.auth_info = JSONEncoder().encode(info)
        d.save(force_update=True)
        sync_weibo.apply_async(args = [did, 1, None], countdown = 84600)

# Renren related sync tasks

@task(ignore_result=True)
def sync_renren_blogs(did, page, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    sig_calc = u"access_token=%sformat=jsonmethod=blog.getspage=%suid=%sv=1.0%s" % (info['access_token'], page, info['user']['id'], RENREN_SECRET)
    sig = calc_md5(sig_calc)
    blogs_url = "http://api.renren.com/restserver.do?method=blog.gets&v=1.0&access_token=%s&format=json&page=%s&uid=%s&sig=%s" % (info['access_token'], page, info['user']['id'], sig)
    blogs_info = JSONDecoder().decode(urllib2.urlopen(blogs_url, "").read())
    
    if blogs_info.has_key('blogs') and blogs_info['blogs']:
        if (page == 1):
            new_latest = blogs_info['blogs'][0]['id']
        for blog in blogs_info['blogs']:
            if (info.has_key('latest_blog') and blog['id'] == info['latest_blog']):
                info['latest_blog'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_renren_blogs.apply_async(args = [did, 1, None], countdown = 84600)
                sync_renren_status.apply_async(args = [d.id, 1, None], countdown = 1)
                break
            sig_calc = u"access_token=%sformat=jsonid=%smethod=blog.getuid=%sv=1.0%s" % (info['access_token'], blog['id'], info['user']['id'], RENREN_SECRET)
            sig = calc_md5(sig_calc)
            blog_url = "http://api.renren.com/restserver.do?method=blog.get&v=1.0&access_token=%s&format=json&id=%s&uid=%s&sig=%s" % (info['access_token'], blog['id'], info['user']['id'], sig)
            blog_info = JSONDecoder().decode(urllib2.urlopen(blog_url, "").read())
            p = Paw.objects.create(source=d,\
                                   type="renren blog",\
                                   title=blog_info['title'],\
                                   summary=blog['content'],\
                                   content=blog_info['content'],\
                                   create_time=datetime.strptime(blog_info['time'], "%Y-%m-%d %H:%M:%S"))
        if not (info.has_key('latest_blog') and blog['id'] == info['latest_blog']):
            sync_renren_blogs.apply_async(args = [did, page+1, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest_blog'] = new_latest
        d.auth_info = JSONEncoder().encode(info)
        d.save(force_update=True)
        sync_renren_blogs.apply_async(args = [did, 1, None], countdown = 84600)
        sync_renren_status.apply_async(args = [d.id, 1, None], countdown = 1)

@task(ignore_result=True)
def sync_renren_status(did, page, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    sig_calc = u"access_token=%scount=1000format=jsonmethod=status.getspage=%suid=%sv=1.0%s" % (info['access_token'], page, info['user']['id'], RENREN_SECRET)
    sig = calc_md5(sig_calc)
    statues_url = "http://api.renren.com/restserver.do?method=status.gets&v=1.0&access_token=%s&count=1000&format=json&page=%s&uid=%s&sig=%s" % (info['access_token'], page, info['user']['id'], sig)
    statues = JSONDecoder().decode(urllib2.urlopen(statues_url, "").read())
    if statues:
        if (page == 1):
            new_latest = statues[0]['status_id']
        for status in statues:
            if info.has_key('latest_status') and status['status_id'] == info['latest_status']:
                info['latest_status'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_renren_status.apply_async(args = [did, 1, None], countdown = 84600)
                sync_renren_albums.apply_async(args = [d.id, 1], countdown = 1)
                break
            p = Paw.objects.create(source=d,\
                                   type="renren status",\
                                   content=status['message'],\
                                   create_time=datetime.strptime(status['time'], "%Y-%m-%d %H:%M:%S"))
        if not (info.has_key('latest_status') and status['status_id'] == info['latest_status']):
            sync_renren_status.apply_async(args = [did, page+1, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest_status'] = new_latest
        d.auth_info = JSONEncoder().encode(info)
        d.save(force_update=True)
        sync_renren_status.apply_async(args = [did, 1, None], countdown = 84600)
        sync_renren_albums.apply_async(args = [d.id, 1], countdown = 1)

@task(ignore_result=True)
def sync_renren_albums(did, page, info=None):
    d = DataSource.objects.get(pk=did)
    if info == None:
        info = JSONDecoder().decode(d.auth_info)
    sig_calc = u"access_token=%scount=1000format=jsonmethod=photos.getAlbumspage=%suid=%sv=1.0%s" % (info['access_token'], page, info['user']['id'], RENREN_SECRET)
    sig = calc_md5(sig_calc)
    albums_url = "http://api.renren.com/restserver.do?method=photos.getAlbums&v=1.0&access_token=%s&count=1000&format=json&page=%s&uid=%s&sig=%s" % (info['access_token'], page, info['user']['id'], sig)
    albums = JSONDecoder().decode(urllib2.urlopen(albums_url, "").read())
    if albums:
        for album in albums:
            if str(album['aid']) in info['albums']:
                p = Paw.objects.get(pk=info['albums'][str(album['aid'])])
                p.title = album['name']
                p.summary = album['description']
            else:
                p = Paw.objects.create(source=d,\
                                       type="renren album",\
                                       title=album['name'],\
                                       summary=album['description'],\
                                       content='{}',\
                                       create_time=datetime.strptime(album['create_time'], "%Y-%m-%d %H:%M:%S"))
                info['albums'][str(album['aid'])] = p.id
            sync_renren_photos.apply_async(args = [p.id, 1, album['size'], info, album], countdown = 1)
        sync_renren_albums.apply_async(args = [did, page+1, info], countdown = 60)
    else:
        d.auth_info = JSONEncoder().encode(info)
        d.save(force_update=True)
        sync_renren_albums.apply_async(args = [did, 1], countdown = 84600)

@task(ignore_result=True)
def sync_renren_photos(pid, page, left, info, album):
    p = Paw.objects.get(pk=pid)
    photo_list = JSONDecoder().decode(p.content)
    sig_calc = u"access_token=%said=%scount=1000format=jsonmethod=photos.getpage=%suid=%sv=1.0%s" % (info['access_token'], album['aid'], page, info['user']['id'], RENREN_SECRET)
    sig = calc_md5(sig_calc)
    photos_url = "http://api.renren.com/restserver.do?method=photos.get&v=1.0&access_token=%s&aid=%s&count=1000&format=json&page=%s&uid=%s&sig=%s" % (info['access_token'], album['aid'], page, info['user']['id'], sig)
    photos = JSONDecoder().decode(urllib2.urlopen(photos_url, "").read())
    for photo in photos:
        if not str(photo['pid']) in photo_list:
            new_img = Img(album = p, title=photo['caption'], upload_time=datetime.strptime(photo['time'], "%Y-%m-%d %H:%M:%S"))
            origin_tmp = NamedTemporaryFile(delete=True)
            origin_tmp.write(urllib2.urlopen(photo['url_large']).read())
            origin_tmp.flush()
            new_img.original.save(origin_tmp.name.split('/')[-1]+'.jpg', File(origin_tmp), save=False)
            thumb_tmp = NamedTemporaryFile(delete=True)
            thumb_tmp.write(urllib2.urlopen(photo['url_head']).read())
            thumb_tmp.flush()
            new_img.thumbnail.save(thumb_tmp.name.split('/')[-1]+'.jpg', File(thumb_tmp), save=True)
            photo_list[str(photo['pid'])] = new_img.id
    left -= 1000
    p.content = JSONEncoder().encode(photo_list)
    p.save(force_update=True)
    if (left > 0):
        sync_renren_photos.apply_async(args=[pid, page+1, left, info, album], countdown = 60)

# RSS sync task

@task(ignore_result=True)
def sync_rss(did):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    f = feedparser.parse(info['url'])
    for entry in f["entries"]:
        # If the item didn't come with a GUID, then
        # use link and then title as an identifier.
            if not "id" in entry:
                if "link" in entry:
                    entry["id"] = entry["link"]
                else:
                    entry["id"] = entry["title"]
            entry["create_time"]=datetime(entry.updated_parsed.tm_year, \
                                          entry.updated_parsed.tm_mon, \
                                          entry.updated_parsed.tm_mday, \
                                          entry.updated_parsed.tm_hour, \
                                          entry.updated_parsed.tm_min, \
                                          entry.updated_parsed.tm_sec)
            if not "content" in entry:
                if "description" in entry:
                    entry["real_content"] = entry["description"]
                else:
                    entry["real_content"] = entry["summary"]
            else:
                entry["real_content"] = entry["content"][0]["value"]
            if (info.has_key('latest') and (entry["id"] == info['latest'])):
                break
            else:
                p = Paw.objects.create(source=d, \
                                       type="rss", \
                                       title=entry["title"][:100], \
                                       summary=entry["summary"], \
                                       content=entry["real_content"], \
                                       create_time=entry["create_time"])
    if f["entries"]:
        info['latest'] = f.entries[0]["id"]
    d.auth_info = JSONEncoder().encode(info)
    d.save(force_update=True)
    sync_rss.apply_async(args = [did], countdown = 84600)

# Douban related sync tasks

@task(ignore_result=True)
def sync_douban_notes(did, index, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    consumer = oauth.Consumer(key=DOUBAN_KEY, secret=DOUBAN_SECRET)
    token = oauth.Token(key=info['oauth_token'], secret=info['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    url = "http://api.douban.com/people/%s/notes?start-index=%s&max-results=50&alt=json" % (info['douban_user_id'], index)
    resp, content = client.request(url, "GET")
    notes_info = JSONDecoder().decode(content)
    
    if notes_info['entry']:
        if (index == 1):
            new_latest = notes_info['entry'][0]['id']['$t']
        for note in notes_info['entry']:
            if (info.has_key('latest_note') and note['id']['$t'] == info['latest_note']):
                info['latest_note'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_douban_notes.apply_async(args = [did, 1, None], countdown = 84600)
                sync_douban_reviews.apply_async(args = [did, 1, None], countdown = 1)
                break
            new_paw = Paw.objects.create(source=d, \
                                         type="douban note", \
                                         title=note['title']['$t'], \
                                         summary=note['summary']['$t'], \
                                         content=note['content']['$t'], \
                                         create_time=datetime.strptime(note['published']['$t'][:-6], "%Y-%m-%dT%H:%M:%S"))
        if not (info.has_key('latest_note') and note['id']['$t'] == info['latest_note']):
            sync_douban_notes.apply_async(args = [did, index+50, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest_note'] = new_latest
            d.auth_info = JSONEncoder().encode(info)
            d.save(force_update=True)
        sync_douban_notes.apply_async(args = [did, 1, None], countdown = 84600)
        sync_douban_reviews.apply_async(args = [did, 1, None], countdown = 1)

@task(ignore_result=True)
def sync_douban_reviews(did, index, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    consumer = oauth.Consumer(key=DOUBAN_KEY, secret=DOUBAN_SECRET)
    token = oauth.Token(key=info['oauth_token'], secret=info['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    url = "http://api.douban.com/people/%s/reviews?start-index=%s&max-results=50&alt=json" % (info['douban_user_id'], index)
    resp, content = client.request(url, "GET")
    reviews_info = JSONDecoder().decode(content)
    
    if reviews_info['entry']:
        if (index == 1):
            new_latest = reviews_info['entry'][0]['id']['$t']
        for review in reviews_info['entry']:
            if (info.has_key('latest_review') and review['id']['$t'] == info['latest_review']):
                info['latest_review'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_douban_reviews.apply_async(args = [did, 1, None], countdown = 84600)
                sync_douban_collections.apply_async(args = [did, 1, None], countdown = 1)
                break
            
            #get the specific review's content
            review_url = review['id']['$t']+"?alt=json"
            resp, content = client.request(review_url, "GET")
            review_content = JSONDecoder().decode(content)
            
            new_paw = Paw.objects.create(source=d, \
                                         type="douban review", \
                                         title=review['title']['$t'], \
                                         summary=review['summary']['$t'], \
                                         content=review_content['content']['$t'], \
                                         create_time=datetime.strptime(review['published']['$t'][:-6], "%Y-%m-%dT%H:%M:%S"))
        if not (info.has_key('latest_review') and review['id']['$t'] == info['latest_review']):
            sync_douban_reviews.apply_async(args = [did, index+50, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest_review'] = new_latest
            d.auth_info = JSONEncoder().encode(info)
            d.save(force_update=True)
        sync_douban_reviews.apply_async(args = [did, 1, None], countdown = 84600)
        sync_douban_collections.apply_async(args = [did, 1, None], countdown = 1)
        
@task(ignore_result=True)
def sync_douban_collections(did, index, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    consumer = oauth.Consumer(key=DOUBAN_KEY, secret=DOUBAN_SECRET)
    token = oauth.Token(key=info['oauth_token'], secret=info['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    url = "http://api.douban.com/people/%s/collection?start-index=%s&max-results=50&alt=json" % (info['douban_user_id'], index)
    resp, content = client.request(url, "GET")
    collections_info = JSONDecoder().decode(content)
    
    if collections_info['entry']:
        if (index == 1):
            new_latest = collections_info['entry'][0]['id']['$t']
        for collect in collections_info['entry']:
            if (info.has_key('latest_collection') and collect['id']['$t'] == info['latest_collection']):
                info['latest_collection'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_douban_collections.apply_async(args = [did, 1, None], countdown = 84600)
                break
            new_paw = Paw.objects.create(source=d, \
                                         type="douban collection", \
                                         content=collect['title']['$t'], \
                                         create_time=datetime.strptime(collect['updated']['$t'][:-6], "%Y-%m-%dT%H:%M:%S"))
        if not (info.has_key('latest_collection') and collect['id']['$t'] == info['latest_collection']):
            sync_douban_collections.apply_async(args = [did, index+50, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest_collection'] = new_latest
            d.auth_info = JSONEncoder().encode(info)
            d.save(force_update=True)
        sync_douban_collections.apply_async(args = [did, 1, None], countdown = 84600)

# Tecent Weibo sync task

@task(ignore_result=True)
def sync_tqq(did, flag, time, lid, new_latest):
    d = DataSource.objects.get(pk=did)
    info = JSONDecoder().decode(d.auth_info)
    consumer = oauth.Consumer(key=QQ_KEY, secret=QQ_SECRET)
    token = oauth.Token(key=info['oauth_token'], secret=info['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    url = "http://open.t.qq.com/api/statuses/broadcast_timeline?format=json&pageflag=%s&reqnum=200&pagetime=%s&lastid=%s&type=1&contenttype=0&accesslevel=1" % (flag, time, lid)
    resp, content = client.request(url, "GET")
    posts_info = JSONDecoder().decode(content)
    
    if posts_info['data']:
        if (flag == 0):
            new_latest = posts_info['data']['info'][0]['id']
        for post in posts_info['data']['info']:
            if (info.has_key('latest') and post['id'] == info['latest']):
                info['latest'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                sync_tqq.apply_async(args=[did, 0, 0, 0, None], countdown = 84600)
                break
            new_paw = Paw.objects.create(source=d, \
                                         type="tqq", \
                                         content=post['text'], \
                                         create_time=datetime.fromtimestamp(post['timestamp']))
            if post['image']:
                for img_url in post['image']:
                    new_img = Img(album = new_paw, upload_time=datetime.fromtimestamp(post['timestamp']))
                    origin_tmp = NamedTemporaryFile(delete=True)
                    origin_tmp.write(urllib2.urlopen(img_url+"/160").read())
                    origin_tmp.flush()
                    new_img.original.save(origin_tmp.name.split('/')[-1]+'.jpg', File(origin_tmp), save=False)
                    thumb_tmp = NamedTemporaryFile(delete=True)
                    thumb_tmp.write(urllib2.urlopen(img_url+"/2000").read())
                    thumb_tmp.flush()
                    new_img.thumbnail.save(thumb_tmp.name.split('/')[-1]+'.jpg', File(thumb_tmp), save=True)
                    new_img.save()
        
        if not (info.has_key('latest') and post['id'] == info['latest']):
            sync_tqq.apply_async(args=[did, 1, post['timestamp'], post['id'], new_latest], countdown = 1)
    else:
        info['latest'] = new_latest
        d.auth_info = JSONEncoder().encode(info)
        d.save(force_update=True)
        sync_tqq.apply_async(args=[did, 0, 0, 0, None], countdown = 84600)
        
# Taobao sync task

@task(ignore_result=True)
def sync_taobao(did, page, new_latest):
    d = DataSource.objects.get(pk=did)
    
    # here refresh the sessionkey
    
    info = JSONDecoder().decode(d.auth_info)
    sign_str = "appkey"+TAOBAO_KEY+"refresh_token"+info['refresh_token']+"sessionkey"+info['top_session']+TAOBAO_SECRET
    hash = md5.new()
    hash.update(sign_str)
    sign = hash.hexdigest().upper()
    access_token_url = 'http://container.open.taobao.com/container/refresh?appkey=%s&refresh_token=%s&sessionkey=%s&sign=%s' \
                       % (TAOBAO_KEY, info['refresh_token'], info['top_session'], sign)
    new_info = JSONDecoder().decode(urllib2.urlopen(access_token_url, "").read())
    info['top_session'] = new_info['top_session']
    info['refresh_token'] = new_info['refresh_token']
    d.auth_info = JSONEncoder().encode(info)
    d.save(force_update=True)
    
    # here begin the goods sync
    info = JSONDecoder().decode(d.auth_info)
    params = {
                        'method':'taobao.trades.bought.get',
                        'session':info['top_session'],
                        'fields':'tid,created,seller_nick,orders.oid,orders.pic_path,orders.total_fee,orders.title',
                        'partner_id':'top-apitools',
                        'format':'json',
                        'page_no':page,
                        'status':'TRADE_FINISHED'
                    }

    op = OpenTaobao(TAOBAO_KEY,TAOBAO_SECRET)
    deal_info = JSONDecoder().decode(op.get_result(params))['trades_bought_get_response']
    
    if deal_info.has_key('trades') and deal_info['trades']:
        if (page == 1):
            print "now is page1"
            new_latest = deal_info['trades']['trade'][0]['tid']
        for trade in deal_info['trades']['trade']:
            if (info.has_key('latest') and (trade['tid'] == info['latest'])):
                info['latest'] = new_latest
                d.auth_info = JSONEncoder().encode(info)
                d.save(force_update=True)
                
                sync_taobao.apply_async(args = [did, 1, None], countdown = 84000) # wait for tommorow to do again this task
                print "I am break and do it tomorrow"
                break
            
            for order in trade['orders']['order']:
                print "I am in again"
                new_paw = Paw.objects.create(source=d, type="taobao", content=u"在"+trade['seller_nick']+u"店</br>花费"+order['total_fee']+u"</br>购买了"+order["title"], create_time=trade['created'])
                if order.has_key('pic_path'):
                    new_img = Img(album = new_paw, upload_time=new_paw.create_time)
                    origin_tmp = NamedTemporaryFile(delete=True)
                    origin_tmp.write(urllib2.urlopen(order['pic_path']).read())
                    origin_tmp.flush()
                    new_img.original.save(origin_tmp.name.split('/')[-1]+'.jpg', File(origin_tmp), save=False)
                    thumb_tmp = NamedTemporaryFile(delete=True)
                    thumb_tmp.write(urllib2.urlopen(order['pic_path']+'_sum.jpg').read())
                    thumb_tmp.flush()
                    new_img.thumbnail.save(thumb_tmp.name.split('/')[-1]+'.jpg', File(thumb_tmp), save=True)
            
        if not (info.has_key('latest') and (trade['tid'] == info['latest'])):
            print "do it 1min later"
            sync_taobao.apply_async(args = [did, page+1, new_latest], countdown = 60)
    else:
        if new_latest is not None:
            info['latest'] = new_latest
            d.auth_info = JSONEncoder().encode(info)
            d.save(force_update=True)
        print "do it tommorrow"    
        sync_taobao.apply_async(args = [did, 1, None], countdown = 84000)
