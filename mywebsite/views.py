from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    print(request.user)
    gr=request.user.groups.all()
    context={
        "user":request.user,
        "groups":gr 
    }
    for grp in gr:
        print(grp.name)
    return render(request, 'home.html', context=context)

def default_page(request):
    print(request.user)
    return redirect("home")

# @api_view(['GET', 'POST'])
def common(request):
    # return Response(status = status.HTTP_200_OK)
    return render(request, 'common.html')

def success(request):
    # return Response(status = status.HTTP_200_OK)
    return render(request, 'success.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        # Check if the email exists
        if User.objects.filter(email=email).exists():
            # Generate password reset link and send email
            user = User.objects.get(email=email)
            print(user)
        
            reset_token = default_token_generator.make_token(user)

            # Create your reset URL and send it via email
            reset_link = f"http://127.0.0.1:8000/reset-password/{user.pk}/{reset_token}/"

            # reset_url = request.build_absolute_uri(f"/reset_password/{reset_token}/")
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('forgot_password')
        else:
            messages.error(request, "No user is registered with this email address.")
            return redirect('forgot_password')
    
    return render(request, 'forgot_password.html')


def reset_password(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)

        # Validate the token
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('reset_password', user_id=user_id, token=token)

                # Set the new password and save the user
                user.set_password(new_password)
                user.save()

                messages.success(request, "Your password has been reset successfully.")
                return redirect('seeker_login')  # Redirect to login page after reset

            return render(request, 'reset_password.html', {'user_id': user_id, 'token': token})

        else:
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect('seeker_login')  # Redirect to login if token is invalid

    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('seeker_login')  # Redirect to login if user does not exist

