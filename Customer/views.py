from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Utils.role_decoratory import customer_required


@login_required
@customer_required
def customer_dashboard_view(request):
    """
    Customer dashboard with recent bookings
    """
    total_bookings = request.user.bookings.count()
    delivered = request.user.bookings.filter(status='delivered').count()
    pending = request.user.bookings.exclude(status__in=['delivered', 'cancelled']).count()

    active_bookings = request.user.bookings.exclude(status__in=['cancelled']).order_by('-created_at')

    context = {
        'total_bookings': total_bookings,
        'delivered': delivered,
        'pending': pending,
        'bookings': active_bookings,
    }
    return render(request, 'customer/customer_dashboard.html', context)
