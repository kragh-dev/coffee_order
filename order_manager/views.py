from django.http import JsonResponse
from rest_framework import views
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import logging
from django.db.models import F,Q
from django.db.models import Count, Sum
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import User

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
                    role=request.data['role'],)

                user.save()

                return JsonResponse({'status': True,'id': user.id, 'message': 'New user added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)   
        else:
            try:
                user = User.objects.filter(id=userId).update(
                    name=request.data['name'],
                    phone=request.data['phone'],
                    role=request.data['role'])

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
                'status': status
            }) 
        return JsonResponse(result, safe=False, status=200)
   