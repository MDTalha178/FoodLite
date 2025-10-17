from django.shortcuts import render, get_object_or_404

from Booking.models import Booking
from Chat.models import ChatRoom


# Create your views here.
def chat_room_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    chat_room, _ = ChatRoom.objects.get_or_create(
        booking=booking,
        defaults={'customer': booking.customer, 'partner': booking.delivery_partner.user}
    )
    messages = chat_room.messages.all()
    return render(request, 'Booking/chat.html', {'booking': booking, 'messages': messages})