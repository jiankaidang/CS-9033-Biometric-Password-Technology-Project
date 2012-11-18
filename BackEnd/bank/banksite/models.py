from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __unicode__(self):
        return self.uid