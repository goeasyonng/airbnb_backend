from django.shortcuts import render
from django.http import HttpResponse

def see_all_rooms(request):
    return HttpResponse("see all rooms")

def see_one_room(request, room_id,room_name):
    return HttpResponse(f"see one room with id : {room_id}")