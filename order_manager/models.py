from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

class Shops(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)

    def save(self):
        super(Shops, self).save()
        return self

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.IntegerField()
    phone = models.CharField(max_length=10, unique=True)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self):
        super(User, self).save()
        return self

    def __str__(self):
        s=str(self.id)
        return s 

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)

    def __str__(self):
        s=str(self.id)
        return s

class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        s=str(self.id)
        return s

class OrderTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self):
        super(OrderTemplate, self).save()
        return self

class OrderItemStack(models.Model):
    order_temp_id = models.ForeignKey(OrderTemplate, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self):
        super(OrderItemStack, self).save()
        return self

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=True)
    user_id = models.ForeignKey(User, on_delete=True)
    morning_time = models.TimeField()
    evening_time = models.TimeField()
    date = models.DateField()
    order_template_id = models.ForeignKey(OrderTemplate, on_delete=True)

    def save(self):
        super(Schedule, self).save()
        return self

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    delivery_status = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    user_phone = models.IntegerField()
    delivery_date = models.DateField()
    delivery_time = models.TextField()
    total_price = models.IntegerField()


class OrderList(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_list_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.ForeignKey(OrderTemplate, on_delete=True)
    price = models.IntegerField()

class Automate(models.Model):
    run_at_times = models.TimeField()