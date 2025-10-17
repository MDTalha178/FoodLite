from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from Booking.models import Booking
from Utils.role_decoratory import delivery_required


# Create your views here.
@login_required
@delivery_required
def partner_dashboard(request):
    partner_profile = request.user.delivery_partner_profile
    total_bookings = partner_profile.assigned_bookings.count()
    delivered = partner_profile.assigned_bookings.filter(status='delivered').count()
    active_pending = partner_profile.assigned_bookings.exclude(status='delivered').count()

    available_bookings = Booking.objects.filter(status='pending', delivery_partner__isnull=True).order_by('-created_at')

    all_bookings = partner_profile.assigned_bookings.order_by('-created_at')

    context = {
        'total_bookings': total_bookings,
        'delivered': delivered,
        'active_pending': active_pending,
        'available_bookings': available_bookings,
        'all_bookings': all_bookings,
        'partner_status': partner_profile.status
    }
    return render(request, 'DeliveryPartner/partner_dashboard.html', context)


@login_required
@delivery_required
def accept_booking(request, booking_id):
    partner_profile = request.user.delivery_partner_profile
    booking = get_object_or_404(Booking, id=booking_id)

    if partner_profile.status not in ['available', 'online']:
        messages.error(request, "You cannot accept a new delivery while busy or offline.")
        return redirect('partner_dashboard')

    booking.delivery_partner = partner_profile
    booking.status = 'assigned'
    booking.save()

    partner_profile.status = 'busy'
    partner_profile.current_booking = booking
    partner_profile.save()

    messages.success(request, f"You have accepted Booking #{booking.id}")
    return redirect('partner_dashboard')


@login_required
@delivery_required
def update_booking_status(request, booking_id):
    partner_profile = request.user.delivery_partner_profile
    booking = get_object_or_404(Booking, id=booking_id, delivery_partner=partner_profile)

    STATUS_SEQUENCE = ['assigned', 'started', 'reached', 'collected', 'delivered']

    if booking.status not in STATUS_SEQUENCE:
        messages.error(request, "Cannot update status for this booking.")
        return redirect('partner_dashboard')

    current_index = STATUS_SEQUENCE.index(booking.status)
    if current_index < len(STATUS_SEQUENCE) - 1:
        booking.status = STATUS_SEQUENCE[current_index + 1]
        booking.save()
        messages.success(request, f"Booking #{booking.id} status updated to {booking.status.title()}.")

    # If delivered, make partner available again
    if booking.status == 'delivered':
        partner_profile.status = 'available'
        partner_profile.current_booking = None
        partner_profile.save()

    return redirect('partner_dashboard')
