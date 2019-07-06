from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

class Shops(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def _str_(self):
        return self.branch


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.IntegerField(max_length=1)
    phone = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self):
        super(User, self).save()
        return self


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    client_phone = models.IntegerField(max_length=10, unique=True)
    branch = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)
    price = models.IntegerField(max_length=10)


class OrderTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=10)

class Schedule(models.Model):
    client_id = models.ForeignKey(Client, on_delete=True)
    user_id = models.ForeignKey(User, on_delete=True)
    user_phone = models.IntegerField()
    morning_time = models.TextField()
    evening_time = models.TimeField()
    date = models.DateField()
    order_template_id = models.ForeignKey(OrderTemplate, on_delete=True)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(max_length=6)
    delivery_status = models.IntegerField(max_length=1)
    date = models.DateField()
    time = models.TimeField()
    user_phone = models.IntegerField()
    delivery_date = models.DateField()
    delivery_time = models.TextField()
    total_price = models.IntegerField(max_length=10)


class OrderList(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_list_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.ForeignKey(OrderTemplate, on_delete=True)
    price = models.IntegerField()