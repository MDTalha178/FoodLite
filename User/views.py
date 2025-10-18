from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from DeliveryPartner.models import DeliveryPartner
from User.models import User, OTPVerification

STATIC_OTP = '1234'


@require_http_methods(["GET"])
def home_view(request):
    return render(request, 'accounts/home.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    Handle user registration
    """
    if request.method == 'POST':
        mobile = request.POST.get('mobile_number', '').strip()
        role = request.POST.get('role', 'customer')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not mobile or not first_name:
            messages.error(request, 'Mobile number and name are required.')
            return render(request, 'accounts/register.html', {'roles': User.ROLE_CHOICES})

        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Mobile number already registered.')
            return render(request, 'accounts/register.html', {'roles': User.ROLE_CHOICES})

        # Generate and store OTP
        otp = STATIC_OTP  # Static OTP for development
        expires_at = timezone.now() + timedelta(minutes=10)

        OTPVerification.objects.filter(
            mobile_number=mobile,
            is_verified=False
        ).delete()

        otp_obj = OTPVerification.objects.create(
            mobile_number=mobile,
            otp=otp,
            expires_at=expires_at
        )
        user = User.objects.create(
            username=mobile,
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_verified=False,
        )

        # create profile for Delivery Partner
        if role == 'partner':
            DeliveryPartner.objects.update_or_create(
                user_id=user.id,
                defaults={
                    'status': 'online'
                }
            )

        request.session['otp_id'] = str(otp_obj.id)
        return redirect('verify_otp')

    return render(request, 'accounts/register.html', {'roles': User.ROLE_CHOICES})


@require_http_methods(["GET", "POST"])
def verify_otp_view(request):
    """
    Verify OTP during registration
    """
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        otp_id = request.session.get('otp_id')

        is_login_request = request.session.get('is_login', False)

        if not otp_id:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('login')

        try:
            otp_obj = OTPVerification.objects.get(id=otp_id)
        except OTPVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP request.')
            return redirect('login')

        if otp_obj.is_expired():
            messages.error(request, 'OTP expired. Please register again.')
            return redirect('login')

        if otp_obj.attempts >= 3:
            messages.error(request, 'Too many attempts. Please register again.')
            return redirect('login')

        otp_obj.attempts += 1
        otp_obj.save()

        if entered_otp == otp_obj.otp:
            otp_obj.is_verified = True
            otp_obj.save()

            user = User.objects.get(mobile=otp_obj.mobile_number)
            user.is_verified = True
            user.save()

            login(request, user)

            # If delivery partner, create profile
            if user.role == 'customer':
                return redirect('customer_dashboard')
            if user.role == 'partner':
                return redirect('partner_dashboard')

            if user.role == 'admin':
                return redirect('admin_dashboard')

            messages.success(request, 'Registration successful! Please login.')
            del request.session['otp_id']
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'accounts/verify_otp.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Handle user login via mobile number and OTP
    """
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number', '').strip()

        try:
            user = User.objects.get(mobile=mobile_number)
        except User.DoesNotExist:
            messages.error(request, 'Mobile number not registered.')
            return render(request, 'accounts/login.html')

        # Generate OTP
        otp = STATIC_OTP
        expires_at = timezone.now() + timedelta(minutes=10)

        OTPVerification.objects.filter(
            mobile_number=mobile_number,
            is_verified=False
        ).delete()

        otp_obj = OTPVerification.objects.create(
            mobile_number=mobile_number,
            otp=otp,
            expires_at=expires_at
        )

        request.session['otp_id'] = str(otp_obj.id)
        request.session['is_login'] = True

        messages.info(request, f'OTP sent to {mobile_number}')
        return render(request, 'accounts/verify_otp.html', {'mobile': mobile_number})

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    Logs out the user and redirects to login page.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
