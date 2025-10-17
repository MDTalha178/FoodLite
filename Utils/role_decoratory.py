from django.contrib import messages
from django.shortcuts import redirect


def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_customer():
            messages.error(request, 'Access denied. Customer role required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def delivery_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_delivery_partner():
            messages.error(request, 'Access denied. Delivery Partner role required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_user():
            messages.error(request, 'Access denied. Admin role required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
