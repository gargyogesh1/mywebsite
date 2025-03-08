from django.shortcuts import render
from email import errors
from django.shortcuts import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from .models import *
from mywebsite.models import *

# Create your views here.

import requests
from django.shortcuts import redirect
from django.conf import settings

# Step 1: Redirect user to Google Auth URL
def google_login(request):
    print("google_login work")

    client_id = settings.GOOGLE_CLIENT_ID
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    scope = 'email profile'
    response_type = 'code'

    auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        f'client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}'
    )
    return redirect(auth_url)

# Step 2: Handle Google callback and get user info
def google_callback(request):
    print("google callback")
    code = request.GET.get('code')

    if not code:
        return redirect('error_page')  # Redirect to an error page if something goes wrong.

    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()
    access_token = token_info.get('access_token')


    # Use the access token to get user info
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info = requests.get(user_info_url, headers=headers).json()
    print(user_info)
    # Example: Display user info
    return redirect('home')  # Replace 'home' with your desired redirect after login.
