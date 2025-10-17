from django.db import models
from User.models import User

from django.db import models
from Booking.models import Booking
from Utils.models import BaseModel


class ChatRoom(BaseModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="chat_room")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_chats")
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partner_chats")

    def __str__(self):
        return f"ChatRoom for Booking {self.booking.id}"


class Message(BaseModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username}"