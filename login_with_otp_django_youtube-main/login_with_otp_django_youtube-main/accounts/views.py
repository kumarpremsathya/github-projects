from django.shortcuts import render , redirect

from django.contrib.auth.models import User

from .models import Profile
import random

import http.client

from django.conf import settings
from django.contrib.auth import authenticate, login
import sys

# Create your views here.

def send_otp(mobile, otp):
    try:
        print("FUNCTION CALLED")
        conn = http.client.HTTPSConnection("api.msg91.com")
        authkey = settings.AUTH_KEY  
        headers = {'content-type': "application/json"}
        url = "/api/v5/otp/verify?otp=" + otp + "&mobile=" + mobile
        # Print constructed URL and authentication key
        print("Constructed URL:", conn.host + url)
        print("Authentication Key:", authkey)
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        print(data)
        return data
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Exception Details: {e}")
        return None

def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        
        user = Profile.objects.filter(mobile = mobile).first()
        
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'login.html' , context)
        
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')        
    return render(request,'login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request , user)
            return redirect('cart')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'login_otp.html' , context)
    
    return render(request,'login_otp.html' , context)
    
    
def register(request):
    if request.method == 'POST':
        try:  
            email = request.POST.get('email')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            
            check_user = User.objects.filter(email=email).first()
            check_profile = Profile.objects.filter(mobile=mobile).first()
            
            if check_user or check_profile:
                context = {'message': 'User already exists', 'class': 'danger'}
                return render(request, 'register.html', context)
                
            # Set the username to the email
            username = email
            
            user = User.objects.create_user(username=username, email=email, first_name=name)
            otp = str(random.randint(1000, 9999))
            profile = Profile(user=user, mobile=mobile, otp=otp) 
            profile.save()
            result=send_otp(mobile, otp)
            print("result==", result)
            request.session['mobile'] = mobile
            return redirect('otp')
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Error occurred at line {exc_tb.tb_lineno}:")
            print(f"Exception Type: {exc_type}")
            print(f"Exception Object: {exc_obj}")
            print(f"Traceback: {exc_tb}")
            context = {'message': 'An error occurred while processing your request.', 'class': 'danger'}
            return render(request, 'register.html', context)
            
    return render(request, 'register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            return redirect('cart')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'otp.html' , context)
            
        
    return render(request,'otp.html' , context)