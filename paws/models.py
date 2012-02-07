from django.db import models
from django.utils.encoding import smart_unicode
from timepaw.datasources.models import DataSource

class Paw(models.Model):
    source = models.ForeignKey(DataSource)
    type = models.CharField(max_length = 50)
    title = models.CharField(max_length = 100, blank = True)
    summary = models.TextField(blank = True)
    content = models.TextField(blank = True)
    #origin_link = models.URLField(blank = True)
    create_time = models.DateTimeField()

class Img(models.Model):
    title = models.CharField(max_length = 300, blank = True)
    album = models.ForeignKey(Paw)
    original = models.ImageField(max_length = 300, upload_to = lambda i, fn: i.album.source.owner.email+'/'+smart_unicode(i.album.source.source_name)+'/'+smart_unicode(i.album.source.id)+'/'+smart_unicode(i.album.id)+'/'+fn)
    thumbnail = models.ImageField(max_length = 300, upload_to = lambda i, fn: i.album.source.owner.email+'/'+smart_unicode(i.album.source.source_name)+'/'+smart_unicode(i.album.source.id)+'/'+smart_unicode(i.album.id)+'/'+fn)
    upload_time = models.DateTimeField(blank=True)