from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import auth
from django.utils import timezone
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from gmail_services import send_email
from google_auth_oauthlib.flow import Flow
import os
import uuid
import json

from account.models import CustomUser, ProfileIcon



def Account(request):
    user = request.user
    csrf_token = get_token(request)
    user_authenticated = getattr(user, 'is_authenticated', None)
    username = getattr(user, 'username', None)
    email = getattr(user, 'email', None)
    icon = getattr(user, 'profile_icon', None)

    return JsonResponse({
        'token': csrf_token,
        'authenticated': user_authenticated,
        'username': username,
        'email': email,
        'icon': icon.source if icon else None
        }, content_type='application/json')


def Icons(request):
    icons = ProfileIcon.objects.all()

    # Serialize the data
    icons_list = list(icons.values('id', 'source'))

    # Return as JSON response
    return JsonResponse({'icons': icons_list}, content_type='application/json')


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

    icon = ProfileIcon.objects.get(pk=data.get('icon'))

    user = CustomUser.objects.create(
        username=data.get('username'),
        email=data.get('email'),
        password=make_password(data.get('password')),
        profile_icon=icon,
    )
 
    if user is not None:
        auth.login(request, user)
        return JsonResponse({'message': 'Signup successful'}, status=201)
    else: 
        return JsonResponse({'error': 'Signup unsuccessful'}, status=400)


def UpdateUserInfo(request):
    data = json.loads(request.body.decode('utf-8'))
    
    email = data.get('email', None)
    nickname = data.get('nickname', None)
    icon = data.get('icon', None)

    if email:
        user = request.user
        user.email = email
        user.save()

        return JsonResponse({'success': 'Email updated successfully'})

    if nickname:
        user = request.user
        user.username = nickname
        user.save()

        return JsonResponse({'success': 'Nickname updated successfully'})

    if icon:
        user = request.user
        icon = ProfileIcon.objects.get(pk=data.get('icon'))
        user.profile_icon = icon
        user.save()

        return JsonResponse({'success': 'Profile icon updated successfully'})

    else:
        return JsonResponse({'error': 'Update unsuccessful'}, status=400)



def SendResetEmail(request):
    data = json.loads(request.body.decode('utf-8'))
    myToken = uuid.uuid4().hex

    try:
        userEmail = data.get('email')

        user = CustomUser.objects.get(email=userEmail)
        hashedToken = hash(myToken)
        user.reset_token = hashedToken
        user.reset_token_created_at = timezone.now()
        user.save()

        # when they submit the form again, we still send the token and check again for the user, to prevent data leaks

        if not user:
            return HttpResponse(status=200)

        try:
            send_email(
                subject='Test Subject',
                body=f'https://run-router.netlify.app/password-reset-redirect?t={myToken}',
                to=userEmail
            )
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=200)
    


def oauth2callback(request):
    state = request.GET.get('state')
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), 'credentials.json'),
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        state=state)
    flow.redirect_uri = 'https://run-router-django-8d8af4387754.herokuapp.com/oauth2callback'

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

    return HttpResponse("OAuth2 authentication successful. You can close this window.")


def ValidateResetToken(request):
    data = json.loads(request.body.decode('utf-8'))

    token = data.get('token')
    hashedToken = hash(token)

    try:
        user = CustomUser.objects.get(reset_token=hashedToken)
        
        now = timezone.now()
        if now - user.reset_token_created_at <= timedelta(minutes=15):
            return JsonResponse({'isTokenValid': True}, status=200)
        
        return JsonResponse({'isTokenValid': False}, status=200)

    except Exception as e:
        return JsonResponse({'isTokenValid': False}, status=200)


def updateUserPassword(request):
    data = json.loads(request.body.decode('utf-8'))
    token = data.get('token')
    hashedToken = hash(token)

    try:
        user = CustomUser.objects.get(reset_token=hashedToken)

        now = timezone.now()
        if now - user.reset_token_created_at > timedelta(minutes=15):
            return JsonResponse({'message': 'Token Expired'}, status=500)
        
        password = data.get('password')
        user.password = make_password(password)
        user.reset_token = None
        user.reset_token_created_at = None
        
        user.save()
        
        return JsonResponse({'message': 'Password updated successfully'}, status=200)
        
    except Exception as e:
        return JsonResponse({'message': 'There has been an error, please try again'}, status=500)


def DeleteAccount(request):
    try:
        user = request.user
        user.delete()
        return HttpResponse({'account deleted'}, content_type='application/json')
        
    except Exception as e:
        return HttpResponse({'something went wrong'}, content_type='application/json')
    