from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import auth
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from account.models import CustomUser

import json


def Account(request):
    csrf_token = get_token(request)
    user_authenticated = getattr(request.user, 'is_authenticated', None)
    username = getattr(request.user, 'username', None)
    email = getattr(request.user, 'email', None)
    # print(request.user.icon)

    return JsonResponse({
        'token': csrf_token,
        'authenticated': user_authenticated,
        'username': username,
        'email': email
        }, content_type='application/json')


def LogInUser(request):
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


def LogOutUser(request):
    auth.logout(request)
    return HttpResponse({'logout succesfull'}, content_type='application/json')
    

def SignUpUser(request):
    data = json.loads(request.body.decode('utf-8'))

    user = CustomUser.objects.create(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        icon=data.get('icon'),
    )

    if user is not None:
        auth.login(request, user)
        return JsonResponse({'message': 'Signup successful'}, status=201)
    else:
       return JsonResponse({'error': 'Signup unsuccessful'}, status=400)


def UpdateUserInfo(request):
    data = json.loads(request.body.decode('utf-8'))
    
    email = data.get('email', None)
    password = data.get('password', None)
    nickname = data.get('nickname', None)
    icon = data.get('icon', None)

    if email:
        user = request.user
        user.email = email
        user.save()

        return JsonResponse({'success': 'Email updated successfully'})

    if password:
        user = request.user
        user.password = password
        user.save()

        return JsonResponse({'success': 'Password updated successfully'})

    if nickname:
        user = request.user
        user.username = nickname
        user.save()

        return JsonResponse({'success': 'Nickname updated successfully'})

    if icon:
        user = request.user
        user.icon = icon
        user.save()

        return JsonResponse({'success': 'Profile icon updated successfully'})

    else:
        return JsonResponse({'error': 'Update unsuccessful'}, status=400)

