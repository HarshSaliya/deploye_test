from django.shortcuts import render ,redirect 
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
import pyotp
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from  django.http import HttpResponse
from .utils import send_otp 
# Create your views here.


def home(request):
    return render(request,'home.html')

def signupview(request):
    if request.method == 'POST':
        username=request.POST.get('fname')
        email=request.POST.get('email')
        password=request.POST.get('pas')
    

        cuser =User.objects.create_user(username=username , email=email , password= password)
        cuser.save()

        send_otp(request)
        request.session['username']=username

        return redirect('otp')
        
    return render(request ,'signup.html')


def otpview(request):
    if request.method == "POST":
        otp=request.POST['otpp']
        username =request.session['username']

        otp_secret_key =request.session.get('otp_secret_key')
        otp_valid_date =request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
        

            if valid_until >  datetime.now():
               totp=pyotp.TOTP(otp_secret_key , interval=60)
               if totp.verify(otp):
                   user = get_object_or_404(User , username =username)
                   login(request , user)

                   request.session.flush()
                #    del request.session['otp_secret_key']
                #    del request.session['otp_valid_date']

                   return redirect('home')
               else :   
                #    calling_url = request.META.get('HTTP_REFERER') 
                #    message.error(request ,"invalid otp")
                   return HttpResponse("invalid OTP")
            else :
                 return HttpResponse (" Time up")
        else :
             return HttpResponse (" Something Wrong 3")

    return render(request ,'otp.html')

def logout(request):
    logout(request)
    return redirect('login')
