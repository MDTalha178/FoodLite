from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Booking.models import Booking
from DeliveryPartner.models import DeliveryPartner
from User.models import User
from Utils.role_decoratory import admin_required

@login_required
@admin_required
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    total_bookings = bookings.count()
    delivered = bookings.filter(status='delivered').count()
    pending = bookings.filter(status='pending').count()
    assigned = bookings.filter(status='assigned').count()

    delivery_partners = User.objects.filter(role='partner', is_verified=True)

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'delivered': delivered,
        'pending': pending,
        'assigned': assigned,
        'delivery_partners': delivery_partners
    }
    return render(request, 'Admin/admin_dashboard.html', context)


@login_required
@admin_required
def assign_partner(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
        partner_id = request.POST.get("delivery_partner")
        partner = DeliveryPartner.objects.get(id=partner_id)
        booking.delivery_partner = partner
        booking.status = 'assigned'
        booking.assigned_by = 'admin'
        booking.save()

        partner.current_booking = booking
        partner.status = 'busy'
        partner.save()
        return redirect('admin_dashboard')

    delivery_partners = DeliveryPartner.objects.filter(status__in=['online', 'available'])
    return render(request, 'Admin/assign_partner.html', {'booking': booking, 'delivery_partners': delivery_partners})