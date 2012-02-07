from django.db import models

class ActiveKey(models.Model):
    key = models.CharField(max_length = 30, unique = True)
    used = models.BooleanField(default = False)