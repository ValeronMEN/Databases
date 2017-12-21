# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime

# artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
# pub_date = models.DateTimeField('date published')


class Guitar(models.Model):
    guitar_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Shop(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_type = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    shop_description = models.TextField(blank=True)


class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Bill(models.Model):
    bill_id = models.IntegerField(primary_key=True)
    bill_guitar_id = models.ForeignKey(Guitar, on_delete=models.CASCADE) # on_update=models.CASCADE
    bill_shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    bill_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase_datetime = models.DateTimeField(default=datetime.datetime.now())
    price = models.IntegerField()
