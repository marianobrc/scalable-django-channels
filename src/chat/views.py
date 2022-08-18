import os
from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    environment = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.local")
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'ws_protocol': 'ws://' if environment == 'config.settings.local' else 'wss://'
    })
