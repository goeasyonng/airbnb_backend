# from django.shortcuts import render
# from django.http import HttpResponse

# def see_all_rooms(request):
#     return HttpResponse("see all rooms")

# def see_one_room(request, room_id,room_name):
#     return HttpResponse(f"see one room with id : {room_id}")

from rest_framework.views import APIView
from rest_framework.response import Response
from framework.exceptions import NotFound
from .models import Amenity
from .serializers import AmenitySerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        return Response(
            AmenitySerializer(self.get_object(pk)).data,
        )

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
