from django.db import models
from timepaw.profiles.models import Profile

class DataSource(models.Model):
    source_name = models.CharField(max_length = 20)
    auth_info = models.TextField()
    account_name = models.CharField(max_length = 100, blank = True)
    updated = models.DateTimeField(auto_now = True)
    owner = models.ForeignKey(Profile)