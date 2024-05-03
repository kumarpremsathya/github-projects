from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
import sys


def index(request):
    print("Rendering index page")
    return render(request, "index.html")


def signup(request):
    try:
        print("Inside signup function")
        form = RegisterForm()
        if request.method == 'POST':
            print("Handling POST request in signup function")
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account created successfully! An OTP was sent to your Email")
                return redirect("verify-email", username=request.POST['username'])
        context = {"form": form}
        return render(request, "signup.html", context)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Exception Details: {e}")


def verify_email(request, username):
    print("Inside verify_email function")
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()

    if request.method == 'POST':
        print("Handling POST request in verify_email function")
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            print("OTP code is valid")
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                print("Token is not expired")
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("signin")
            else:
                print("Token has expired")
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        # invalid otp code
        else:
            print("Invalid OTP code")
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)

    context = {}
    return render(request, "verify_token.html", context)


def resend_otp(request):
    print("Inside resend_otp function")
    if request.method == 'POST':
        print("Handling POST request in resend_otp function")
        user_email = request.POST["otp_email"]

        if get_user_model().objects.filter(email=user_email).exists():
            print("User email exists")
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # email variables
            subject = "Email Verification"
            message = f"""
                        Hi {user.username}, here is your OTP {otp.otp_code} 
                        it expires in 5 minute, use the url below to redirect back to the website
                        http://127.0.0.1:8000/verify-email/{user.username}

                        """
            sender = "premkumransathya@gmail.com"
            receiver = [user.email, ]

            # send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            print("User email does not exist")
            messages.warning(request, "This email doesn't exist in the database")
            return redirect("resend-otp")

    context = {}
    return render(request, "resend_otp.html", context)


def signin(request):
    print("Inside signin function")
    if request.method == 'POST':
        print("Handling POST request in signin function")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("index")
        else:
            print("Invalid credentials")
            messages.warning(request, "Invalid credentials")
            return redirect("signin")

    return render(request, "login.html")
