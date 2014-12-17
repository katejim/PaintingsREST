from django.db import models

class Pictures(models.Model):
    link = models.CharField(max_length=300, blank=True)
    name = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return self.name





