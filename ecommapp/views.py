import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .models import VendorProfile
from ecommapp.models import VendorProfile
# Register
'''def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        return redirect('login')

    return render(request, 'register.html')'''


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')


# Home (Protected)
@login_required
def home_view(request):
    return render(request, 'home.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

'''def verify_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST['otp']
        reg_data = request.session.get('reg_data')

        if str(reg_data['otp']) == entered_otp:
            user = User.objects.create_user(
                username=reg_data['username'],
                email=reg_data['email'],
                password=reg_data['password']
            )
            user.save()
            del request.session['reg_data']
            return redirect('login')
        else:
            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'verify_otp.html')'''

def verify_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST['otp']
        reg_data = request.session.get('reg_data')

        if str(reg_data['otp']) == entered_otp:
            user = User.objects.create_user(
                username=reg_data['username'],
                email=reg_data['email'],
                password=reg_data['password']
            )
            user.save()
            request.session['vendor_user_id'] = user.id
            del request.session['reg_data']
            return redirect('vendor_details')
        else:
            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP'
            })

    # If not POST, render the verify OTP page
    return render(request, 'verify_otp.html')



def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        otp = random.randint(100000, 999999)

        # store in session
        request.session['reg_data'] = {
            'username': username,
            'email': email,
            'password': password,
            'otp': otp
        }

        send_mail(
            subject="Your Vendor OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return redirect('verify_otp')

    return render(request, 'register.html')



def vendor_details_view(request):
    user_id = request.session.get('vendor_user_id')
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        VendorProfile.objects.create(
            user=user,
            shop_name=request.POST['shop_name'],
            shop_description=request.POST['shop_description'],
            address=request.POST['address'],
            business_type=request.POST['business_type'],
            id_type=request.POST['id_type'],
            id_number=request.POST['id_number'],
            id_proof_file=request.FILES['id_proof_file']
        )
        del request.session['vendor_user_id']
        return redirect('login')

    return render(request, 'vendor_details.html')

'''@login_required
def home_view(request):
    vendor = VendorProfile.objects.get(user=request.user)

    if not vendor.is_approved:
        return render(request, 'not_approved.html')

    return render(request, 'home.html')'''

@login_required
def home_view(request):
    vendor = VendorProfile.objects.get(user=request.user)

    if not vendor.is_approved:
        return redirect('activation')

    return render(request, 'home.html')



def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    vendors = VendorProfile.objects.all()
    return render(request, 'dashboard.html', {
        'vendors': vendors
    })

@user_passes_test(is_admin)
def approve_vendor(request, vendor_id):
    vendor = VendorProfile.objects.get(id=vendor_id)
    vendor.is_approved = True
    vendor.save()
    return redirect('admin_dashboard')

def activation_view(request):
    vendor = VendorProfile.objects.get(user=request.user)

    if request.method == "POST":
        code = request.POST['code']

        if vendor.activation_code == code:
            vendor.is_approved = True
            vendor.save()
            return redirect('home')
        else:
            return render(request, 'ecommapp/activation.html', {
                'error': 'Invalid activation code'
            })

    return render(request, 'activation.html')
