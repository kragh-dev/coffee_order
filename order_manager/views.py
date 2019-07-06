from django.http import JsonResponse
from rest_framework import views
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import logging
from django.db.models import F,Q
from django.db.models import Count, Sum
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

import jwt,json
from datetime import datetime

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token

class UserCreation(views.APIView):
   def post(self, request, userId=0):
      if userId == 0:
            try:
                user = User(
                    name=request.data['name'],
                    phone=request.data['phone'],
                    role=request.data['role'],
                    password=hasher.encode(password=request.data['pin'],
                                        salt='salt',
                                        iterations=50000))

                user.save()

                return JsonResponse({'status': True,'id': user.id, 'message': 'New user added successfully'}, status=200)
            
            except Exception as e:
                return JsonResponse({'message' : str(e),'status': False},status=200)      