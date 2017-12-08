# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# poll = models.ForeignKey(Poll)
# pub_date = models.DateTimeField('date published')
class Guitar(models.Model):
    name = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    ID = models.IntegerField()