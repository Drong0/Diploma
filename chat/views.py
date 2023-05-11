import json

# chat/views.py
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from .models import Chat, Contact

User = get_user_model()


def get_all_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.all().order_by('-timestamp')


def get_user_contact(id):
    user = get_object_or_404(User, id=id)
    print(user)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})

