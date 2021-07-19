
from django.contrib.auth.decorators import login_required
import pyotp
from django.shortcuts import render
from .models import CustomUser, Addresses
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth import authenticate
import random
import base64
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# Create your views here.
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
import re
from products.views import NavBar
from products.models import Category

navbar = NavBar(Category)
navbar_details = navbar.details()


def validate_phone(s):
    num_pattern = re.compile((r"^[6-9]\d{9}$"))
    return num_pattern.match(s)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        request.session['name'] = name
        request.session['email'] = email
        request.session['phone'] = phone
        data = {'name': name, 'email': email, 'phone': phone}
        print(data)
        if(validate_phone(phone)):
            phone = "+91" + phone
            try:
                validate_email(email)
            except ValidationError as e:
                message = list(e)
                messages.warning(request, message[0])
            else:
                if(CustomUser.objects.filter(email=email)):
                    messages.warning(request, f'Email already Exist')
                elif(CustomUser.objects.filter(phone=phone)):
                    messages.warning(request, f'Phone already Exist')
                else:
                    try:
                        validate_password(password)
                    except ValidationError as e:
                        message = list(e)
                        messages.warning(request, message[0])
                    else:
                        user = CustomUser(email=email, name=name, phone=phone)
                        user.set_password(password)
                        user.save()
                        user_login(request, user)
                        return redirect('home')
            return render(request, 'Accounts/signup.html', {'data': data, 'navbar': navbar_details, 'title': 'Sign Up'})
        else:
            messages.warning(request, f'Enter a valid phone number')
        return render(request, 'Accounts/signup.html', {'data': data, 'navbar': navbar_details, 'title': 'Sign Up'})
    return render(request, 'Accounts/signup.html', {'navbar': navbar_details, 'title': 'Sign Up'})


@csrf_exempt
def login(request):
    if request.method == "POST":
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        print(user)
        if user != None:
            user_login(request, user)
            return redirect('home')
        else:
            messages.warning(request, f'Invalid Credentials')
            return render(request, 'Accounts/login.html', {'title': 'Login', 'navbar': navbar_details})
    else:
        return render(request, 'Accounts/login.html', {'title': 'Login', 'navbar': navbar_details})


def logout(request):
    user_logout(request)
    return redirect('login')


@csrf_exempt
def forgot(request):
    if request.method == "POST":
        phone = request.POST['phone']
        phone = "+91" + phone
        key2 = random.randint(1, 999999)
        request.session['key2'] = key2
        user = CustomUser.objects.filter(phone=phone).first()
        print(user.email)
        if(user == None):
            messages.warning(request, f'No Such User')
            return redirect('forgot')

        else:
            request.session['phone'] = phone
            request.session['email'] = user.email
            return redirect('verify')
    return render(request, 'Accounts/forgot.html', {'title': 'Forgot Password', 'navbar': navbar_details})


@csrf_exempt
def verify(request):
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    phone = request.session['phone']
    key1 = base64.b32encode(bytes(phone, 'utf-8'))
    totp = pyotp.HOTP(key1)
    key2 = request.session['key2']
    send_mail('password reset', 'jewelery website password reset otp='+str(totp.at(key2)),
              settings.EMAIL_HOST_USER, [request.session['email']], fail_silently=False)
    print(totp.at(key2))
    if request.method == "POST":
        otp = request.POST['otp']
        if(totp.verify(otp, key2)):
            request.session['otp'] = otp
            return redirect('reset')
        else:
            messages.warning(request, f'Invalid OTP')
            return redirect('verify')
    return render(request, 'Accounts/verify.html', {'title': 'Verify OTP', 'navbar': navbar_details})


@csrf_exempt
def reset(request):
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    if(request.method == 'POST'):
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password2 == password1):
            try:
                validate_password(password1)
            except ValidationError as e:
                message = list(e)
                messages.warning(request, message[0])
            else:
                phone = request.session['phone']
                key1 = base64.b32encode(bytes(phone, 'utf-8'))
                totp = pyotp.HOTP(key1)
                key2 = request.session['key2']
                otp = request.session['otp']
                if(totp.verify(otp, key2)):
                    user = CustomUser.objects.filter(phone=phone).first()
                    user.set_password(password1)
                    user.save()
                    messages.success(request, f'Succesfully changed password')
                    return redirect('login')
                else:
                    messages.warning(request, f'Passwords dont match')
                    return redirect('reset')
    return render(request, 'Accounts/reset.html', {'title': 'Reset Password', 'navbar': navbar_details})


@login_required
@csrf_exempt
def user(request):
    if request.method == "POST":
        # profile
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        # changepassword
        oldpassword = request.POST.get('oldpassword')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # address

        print('{}-{}-{}'.format(username, phone, email))
        print('{}-{}-{}'.format(oldpassword, password, password2))
    addresses = Addresses.objects.filter(user_id=request.user.id)
    return render(request, "Accounts/user.html", {'title': 'Account', 'addresses': addresses, 'navbar': navbar_details})


@login_required
@csrf_exempt
def addaddress(request):
    if request.method == "POST":
        address = Addresses(
            user_id=request.user,
            fullname=request.POST.get('fullname'),
            mobile_no=request.POST.get('mobile_no'),
            pin_code=request.POST.get('pin_code'),
            building_details=request.POST.get('building_details'),
            area_details=request.POST.get('area_details'),
            landmark_details=request.POST.get('landmark_details'),
            town_details=request.POST.get('town_details'),
            state=request.POST.get('state'),
            address_type=request.POST.get('address_type'),
        )
        address.save()
        return redirect('user')
    return redirect('user')


@login_required
@csrf_exempt
def editaddress(request):
    if request.method == "POST":
        address_id, fullname, mobile_no, pin_code, building_details, area_details, landmark_details, town_details, state, address_type = request.POST.dict().values()
        address = Addresses.objects.filter(id=address_id).first()
        address.fullname = fullname
        address.mobile_no = mobile_no
        address.pin_code = pin_code
        address.building_details = building_details
        address.area_details = area_details
        address.landmark_details = landmark_details
        address.town_details = town_details
        address.state = state
        address.address_type = address_type
        address.save()
        return redirect('user')
    return redirect('user')
