from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login')
def room(request, room_name='main'):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })