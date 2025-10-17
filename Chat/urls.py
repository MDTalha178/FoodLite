from django.urls import re_path, path

from Chat.Consumer.BookingChatConsumer import ChatConsumer
from Chat.Consumer.BookingNotificationConsumer import PartnerBookingConsumer
from Chat.views import chat_room_view

websocket_urlpatterns = [
    re_path(r'ws/partner/booking/$', PartnerBookingConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<booking_id>\w+)/$', ChatConsumer.as_asgi()),
]

urlpatterns = [
    path('chat/<int:booking_id>/', chat_room_view, name='chat'),
]
