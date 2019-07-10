from django.http import JsonResponse
from rest_framework import views
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import logging
from django.db.models import F,Q
from django.db.models import Count, Sum
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django_cron import CronJobBase, Schedule
from .models import User, Shops, Items, Client, OrderTemplate, OrderItemStack, Schedule, Order, OrderList

import jwt,json
from datetime import datetime, date

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token

class UserView(views.APIView):
    def post(self, request, userId=0):
        if userId == 0:
            try:
                user = User(
                    name=request.data['name'],
                    phone=request.data['phone'],
                    role=request.data['role'],
                    shop_id=Shops.objects.filter(id=request.data['shopId']).get(),
                    )

                user.save()

                return JsonResponse({'status': True,'id': user.id, 'message': 'New user added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)   
        else:
            try:
                user = User.objects.filter(id=userId).update(
                    name=request.data['name'],
                    phone=request.data['phone'],
                    role=request.data['role'],
                    shop_id=Shops.objects.filter(id=request.data['shopId']).get(),
                    )

                return JsonResponse({'status': True,'id': id, 'message': 'Information updated successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)

    def get(self, request, userId=0):
        if userId==0:
            users = User.objects.all()
        else:
            users = User.objects.filter(id=userId)
        result = []

        for user in users:
            status=True
            if user.is_active == 0:
                status=False

            result.append({
                'id':user.id,
                'name': user.name,
                'phone': user.phone,
                'role': user.role,
                'shop_id':user.shop_id_id,
                'status': status
            }) 
        return JsonResponse(result, safe=False, status=200)

class ShopView(views.APIView):
    def post(self, request, shopId=0):
        if shopId == 0:
            try:
                shop=Shops(
                    branch=request.data['branch'],
                    address=request.data['address']
                )

                shop.save()

                return JsonResponse({'status': True,'id': shop.id, 'message': 'New shop added successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
        else:
            try:
                shop = Shops.objects.filter(id=shopId).update(
                    branch=request.data['branch'],
                    address=request.data['address']
                )

                return JsonResponse({'status': True,'id': id, 'message': 'Information updated successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)
    
    def get(self, request, shopId=0):
        if shopId==0:
            shops = Shops.objects.all()
        else:
            shops = Shops.objects.filter(id=shopId)
        result = []

        for shop in shops:
            status=True
            if shop.is_active == 0:
                status=False

            result.append({
                'id':shop.id,
                'branch': shop.branch,
                'address': shop.address,
                'status': status
            }) 
        return JsonResponse(result, safe=False, status=200)

class ItemView(views.APIView):
    def post(self, request, idemId=0):
        if idemId==0:
            try:
                item = Items(
                    name = request.data['item_name'],
                    shop_id = Shops.objects.filter(id=request.data['shopId']).get(),
                    price = request.data['price']
                )
                item.save()

                return JsonResponse({'status':True, 'id': item.id, 'message': 'Item added successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message': str(e), 'status':False},status=200)
        else:
            try:
                item = Items.objects.filter(id=itemId).update(
                    name = request.data['item_name'],
                    shop_id = Shops.objects.filter(id=request.data['shopId']).get(),
                    price = request.data['price']
                )
                return JsonResponse({'status':True, 'id': items.id, 'message': 'Item updated successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message': str(e), 'status': False,}, status=200)
    def get(self, request, itemId=0):
        if itemId==0:
            items = Items.objects.all()
        else:
            items = Items.objects.filter(id=itemId)
        result = []

        for item in items:
            status= True
            if item.is_active ==0:
                status=False
            result.append({
                'id':item.id,    
                'item_name':item.name,
                'shop_id':item.shop_id_id,
                'price':item.price 
            })
        return JsonResponse(result, safe= False, status=200)

class ClientView(views.APIView):
    def post(self, request, clientId=0):
        if clientId == 0:
            try:
                client = Client(
                    name = request.data['name'],
                    phone = request.data['phone'],
                    contact_person_name = request.data['contact_name'],
                    address = request.data['address'],
                    shop_id = Shops.objects.filter(id=request.data['shopId']).get(),
                )

                client.save()

                order_temp = OrderTemplate(
                    client_id = Client.objects.filter(id=client.id).get(),
                )

                order_temp.save()

                items = json.loads(request.data['items'])

                for item in items:
                    data = OrderItemStack(
                        order_temp_id = OrderTemplate.objects.filter(id=order_temp.id).get(),
                        item_id = Items.objects.filter(id=item['item_id']).get(),
                        quantity = item['quantity'],
                    )
                    data.save()

                dates = json.loads(request.data['dates'])

                for date in dates:
                    schedule = Schedule(
                        client_id = Client.objects.filter(id=client.id).get(),
                        user_id = User.objects.filter(id=request.data['user_id']).get(),
                        morning_time = request.data['morning_time'],
                        evening_time = request.data['evening_time'],
                        morning_schedule = request.data['morning_schedule'],
                        evening_schedule = request.data['evening_schedule'],
                        date = date['date'],
                        order_template_id = OrderTemplate.objects.filter(id=order_temp.id).get(),
                    )
                    schedule.save()

                return JsonResponse({'status':True, 'id': client.id,'order_temp_id': order_temp.id, 'message': 'Client and the respective orders added successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message': str(e), 'status':False},status=200)
    
    def get(self, request, clientId=0):
        try:
            if clientId==0:
               clients = Client.objects.all()
            else:
                clients = Client.objects.filter(id=clientId)

            details = []
            
            for client in clients:
                items = []
                orders = []
                order_temps = OrderTemplate.objects.filter(client_id=client.id)
                for order_temp in order_temps:
                    item = OrderItemStack.objects.filter(order_temp_id=order_temp.id)
                    for i in item:
                        items.append({
                            'item_id': i.item_id.id,
                            'item_name': i.item_id.name,
                            'quantity': i.quantity,
                        })
                    orders.append({
                        'order_temp_id': order_temp.id, 
                        'items': items,
                    })
                
                details.append({
                    'id': client.id,
                    'name': client.name,
                    'phone': client.phone,
                    'contact_person_name': client.contact_person_name,
                    'address': client.address,
                    'shop_branch': client.shop_id.branch,
                    'orders': orders,
                })

            return JsonResponse(details, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)

def generate_daily_order():
    try:
        print("Updating Today's Order")
        todayDate = date.today()
        schedules = Schedule.objects.filter(date=todayDate),
        for schedule in schedules:
            price = 0,
            items = OrderItemStack.objects.filter(order_temp_id=schedule.order_template_id.id)
            for item in items:
                price = price + (item.item_id.price*item.quantity)
            if schedule.morning_schedule == 1:
                order = Order(
                    client_id = schedule.client_id.id,
                    user_id = schedule.user_id.id,
                    otp = 0,
                    delivery_status = 0,
                    user_phone = schedule.user_id.phone,
                    client_phone = schedule.client_id.phone,
                    date = schedule.date,
                    time = schedule.morning_time,
                    order_temp_id = schedule.order_template_id.id,
                    price = price,
                )
                order.save()
                for i in items:
                    order_list = OrderList(
                        order_id = Order.objects.filter(id=order.id).get(),
                        item_id = i.item_id.id,
                        quantity = i.quantity,
                        price = (i.item_id.price)*(i.quantity),
                    )
                    order_list.save()
            if schedule.evening_schedule == 1:
                order = Order(
                    client_id = schedule.client_id,
                    user_id = schedule.user_id,
                    otp = 0,
                    delivery_status = 0,
                    user_phone = schedule.user_id.phone,
                    client_phone = schedule.client_id.phone,
                    date = schedule.date,
                    time = schedule.evening_time,
                    order_temp_id = schedule.order_template_id,
                    price = price,
                )
                order.save()
                for i in items:
                    order_list = OrderList(
                        order_id = Order.objects.filter(id=order.id).get(),
                        item_id = i.item_id.id,
                        quantity = i.quantity,
                        price = (i.item_id.price)*(i.quantity),
                    )
                    order_list.save()
    except Exception as e:
        print("Failed to generate daily order"+str(e))