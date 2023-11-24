from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import auth
from django.middleware.csrf import get_token
from django.contrib.auth.models import User


import json


def Account(request):
    csrf_token = get_token(request)
    user_authenticated = request.user.is_authenticated
    return JsonResponse({'token': csrf_token, 'authenticated': user_authenticated}, content_type='application/json')

def LogIn(request):
    if request.user.is_authenticated:
        return HttpResponse({'youre already logged in'}, content_type='application/json')

    data = json.loads(request.body.decode('utf-8'))

    user = auth.authenticate(
        username=data.get("username"),
        password=data.get("password")
    )
    if user is not None:
        auth.login(user=user, request=request)
        return JsonResponse({'message': 'Login successful'})
    else:
       return JsonResponse({'error': 'Invalid credentials'}, status=400)

def LogOut(request):
    auth.logout(request)
    return HttpResponse({'logout succesfull'}, content_type='application/json')

def SignUp(request):
    data = json.loads(request.body.decode('utf-8'))

    user = User.objects.create(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password')
    )

    if user is not None:
        return JsonResponse({'message': 'Signup successful'}, status=201)
    else:
       return JsonResponse({'error': 'Signup unsuccessful'}, status=400)