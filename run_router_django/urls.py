"""
URL configuration for run_router_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from run_router.views import RunRouter
from account.views import Account, LogOutUser, LogInUser, SignUpUser, UpdateUserInfo, SendResetEmail, ValidateResetToken, updateUserPassword, oauth2callback, DeleteAccount, Icons


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/route-data', RunRouter),
    path('api/account', Account),
    path('api/login', LogInUser),
    path('api/logout', LogOutUser),
    path('api/signup', SignUpUser),
    path('api/icons', Icons),
    path('api/update-account', UpdateUserInfo),
    path('api/delete-account', DeleteAccount),
    path('api/password-reset-email', SendResetEmail),
    path('api/validate-token', ValidateResetToken),
    path('api/password-reset-confirm', updateUserPassword),
    path('oauth2callback', oauth2callback),
]
