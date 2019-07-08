from django.http import JsonResponse
from rest_framework import views
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import logging
from django.db.models import F,Q
from django.db.models import Count, Sum
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import User, Shops, Items, Client, OrderTemplate, OrderItemStack, Schedule

import jwt,json
from datetime import datetime

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
                    shop_id = Shops.objects.filter(id=request.data['shopId']).get(),
                )

                client.save()

                order_temp = OrderTemplate(
                    client_id = client.id
                )

                order_temp.save()

                items = json.loads(request.data['items'])

                for item in items:
                    data = OrderItemStack(
                        order_temp_id = order_temp.id,
                        item_id = Items.objects.filter(id=item['item_id']).get(),
                        quantity = item['quantity']
                    )
                    data.save()

                userId = User.objects.filter(id=request.data['user_id']).get(),
                user = User.objects.filter(id=userId),

                dates = json.loads(request.data['dates'])

                for date in dates:
                    schedule = Schedule(
                        client_id = client.id,
                        phone = user.phone,
                        user_id = userId,
                        morning_time = request.data('morning_time'),
                        evening_time = request.data('evening_time'),
                        date = date['date'],
                        order_template_id = order_temp.id,
                    )
                    schedule.save()

                return JsonResponse({'status':True, 'id': client.id,'order_temp_id': order_temp.id, 'message': 'Client and the respective orders added successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message': str(e), 'status':False},status=200)

    def get(self, request, clientId=0):
        try:
            client = Client.objects.filter(id=clientId)

            order_temps = OrderTemplate.objects.filter(client_id=client.id)

            orders = []

            item = []

            for order_temp in order_temps:
                items = OrderItemStack.objects.filter(order_temp_id=order_temp.id)
                for item1 in items:
                    item.append({
                        'item_name': item1.name,
                        'quantity': item1.quantity,
                    })
                orders.append({
                    'order_temp_id': order_temp.id, 
                    'items': item,
                })

            result = {
                'id': client.id,
                'name': client.name,
                'orders': orders,
            }

            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message' : str(e),'status': False},status=200)







        