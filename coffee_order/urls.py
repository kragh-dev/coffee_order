"""coffee_order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from order_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', views.UserView.as_view()),
    path('api/user/<int:userId>', views.UserView.as_view()),
    path('api/shop', views.ShopView.as_view()),
    path('api/shop/<int:shopId>', views.ShopView.as_view()),
    path('api/item', views.ItemView.as_view()),
    path('api/item/<int:itemId>', views.ItemView.as_view()),
    path('api/client', views.ClientView.as_view()),
    path('api/client/<int:clientId>', views.ClientView.as_view()),
]
