from django.db import models

class Profile(models.Model):
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50)
    nickname = models.CharField(max_length = 20)
    active = models.BooleanField(default = True)
