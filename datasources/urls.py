from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('timepaw.datasources.views',
    url(r'^$', 'manage'),
    url(r'^delete/(?P<did>\d+)/$', 'delete'),
    url(r'^weibo_add$', 'weibo_add'),
    url(r'^weibo_callback$', 'weibo_callback'),
    url(r'^douban_add$', 'douban_add'),
    url(r'^douban_callback$', 'douban_callback'),
    url(r'^rss_add$', 'rss_add'),
    url(r'^renren_add$', 'renren_add'),
    url(r'^renren_callback$', 'renren_callback'),
    url('^tqq_add', 'tqq_add'),
    url('^tqq_callback', 'tqq_callback'),
    url('^taobao_add', 'taobao_add'),
    url('^taobao_callback', 'taobao_callback'),
)