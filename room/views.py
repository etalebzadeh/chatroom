from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from . models import *

# Create your views here.

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, "room/rooms.html", {"rooms": rooms})

from datetime import datetime
@login_required
def room(request, slug):
    timestamp = int(datetime.now().timestamp())

    user = request.user
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]


    return render(request, "room/room.html", {
        "room": room,
        "messages": messages,
        "user": user,
        "timestamp": timestamp,
        })



def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.user:
        message.delete()
    return redirect('room', slug=message.room.slug)