from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 'timepaw.profiles.views.index'),
   url(r'^signup$', 'timepaw.profiles.views.signup'),
   url(r'^login$', 'timepaw.profiles.views.login'),
   url(r'^home$', 'timepaw.paws.views.home'),
   url(r'^dairy$', 'timepaw.paws.views.dairy'),
   url(r'^sync/(?P<did>\d+)/$', 'timepaw.paws.views.sync'),
   url(r'^logout$', 'timepaw.profiles.views.logout'),
   url(r'^activekeys/add$', 'timepaw.activekeys.views.add'),
   url(r'^datasources/', include('timepaw.datasources.urls')),
   url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.STATIC_ROOT,
       }),
   url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
