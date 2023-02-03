# from django.shortcuts import render
# from django.http import HttpResponse

# def see_all_rooms(request):
#     return HttpResponse("see all rooms")

# def see_one_room(request, room_id,room_name):
#     return HttpResponse(f"see one room with id : {room_id}")

from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from .serializers import (
    AmenitySerializer,
    RoomListSeializer,
    RoomDetailSerializer,
)


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
            amenity = serializer.save(owner=request.user)
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


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSeializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is requires")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("THe category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )  # transaction.atomic이 없을 때 코드를 실행할 때마다 쿼리가 즉시 데이터베이스에 반영되었다.
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            # try:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                            # except Amenity.DoesNotExist:
                            #     room.delete()
                            #     raise ParseError(f"Amenity with id {amenity_pk} not found")
                            # room.delete()
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        # 업데이트시키기
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():  # 만약에 유저에게서 받은 값이 유효하다면
            price, rooms, toilets = (  # 다음의 변수들
                request.data.get("price"),  # 유저에게서 받은 데이터를 get로 쿼리를 가져와라
                request.data.get("rooms"),
                request.data.get("toilets"),
            )
            if price:  # 예외처리문으로 해당 값이 음수라면 에러를 띄우는 조건문
                if price < 0:
                    raise ParseError("price 가 음수입니다.")
            if rooms:
                if rooms < 0:
                    raise ParseError("rooms 가 음수입니다.")
            if toilets:
                if toilets < 0:
                    raise ParseError("toileds 가 음수입니다.")

            amenities_pk, category_pk = request.data.get("amenities"), request.data.get(
                "category"
            )
            if amenities_pk:  # 어메니티의 아이디값을 받는다면
                if not isinstance(amenities_pk, list):
                    raise ParseError("리스트가 아니자나~")
                # 리스트로 받은 pk값이 유효하지 않을 떄
                room.amenities.clear()
                for pk in amenities_pk:
                    try:
                        amenity = Amenity.objects.get(pk=pk)
                    except Amenity.DoesNotExist:
                        raise ParseError("해당 아이디값은 없자나~")
                    room.amenities.add(amenity)

            if category_pk:  # 카테고리의 아이디값을 받는다면
                try:
                    category = Category.objects.get(pk=category_pk)
                except Category.DoesNotExist:
                    raise ParseError("카테고리 값이 없자나~")
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("'rooms'가 아니자나~ ")
                room.category = category
            updated_room = serializer.save()
            return Response(
                RoomDetailSerializer(updated_room).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
