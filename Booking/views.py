from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Booking.models import Booking


@login_required
def create_booking_view(request):
    if request.method == "POST":
        pickup = request.POST.get("pickup_location")
        drop = request.POST.get("drop_location")
        food = request.POST.get("food_details")

        booking = Booking.objects.create(
            customer=request.user,
            pickup_location=pickup,
            drop_location=drop,
            food_details=food,
            status='pending'
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "partners",
            {
                "type": "send_booking",
                "booking": {
                    "id": booking.id,
                    "customer": booking.customer.username,
                    "pickup_location": booking.pickup_location,
                    "drop_location": booking.drop_location,
                    "food_details": booking.food_details,
                    "status": booking.status,
                }
            }
        )

        return redirect('customer_dashboard')

    return render(request, 'Booking/booking.html')


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if not booking.can_be_cancelled():
        messages.error(request, "This booking cannot be cancelled.")
        return redirect('customer_dashboard')

    booking.status = 'cancelled'
    booking.save()
    messages.success(request, f"Booking #{booking.id} has been cancelled successfully.")
    return redirect('customer_dashboard')