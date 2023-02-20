from django.conf import settings
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
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)  # get는 모두 통과하게 해주고 나머지는 인증받은 사람만 통과하게 해줌


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

    permission_classes = (IsAuthenticatedOrReadOnly,)  # read_only

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSeializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(
            data=request.data,
        )
        if serializer.is_valid():  # 유효한 값인지 검사
            category_pk = request.data.get("category")  # 유저에게서 받은 카테고리의 아이디 값
            if not category_pk:  # 카테고리의 아이디값 없다면
                raise ParseError("Category is requires")
            try:
                category = Category.objects.get(pk=category_pk)
                if (
                    category.kind == Category.CategoryKindChoices.EXPERIENCES
                ):  # 유저에게 받은 카테고리의 kind가 experience라면
                    raise ParseError("THe category kind should be 'rooms'")
            except Category.DoesNotExist:  # 카테고리 아이디가 기존에 없는 값이라면
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                    )  # transaction.atomic이 없을 때 코드를 실행할 때마다 쿼리가 즉시 데이터베이스에 반영되었다.
                    room.category = category
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(
                        room,
                    )
                    return Response(serializer.data)
            except Amenity.DoesNotExist:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)


class RoomDetail(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk=pk)
        if room.owner != request.user:
            raise PermissionDenied
        # 업데이트시키기

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():  # 만약에 유저에게서 받은 값이 유효하다면
            with transaction.atomic():
                price, rooms, toilets = (  # 다음의 변수들
                    request.data.get("price"),  # 유저에게서 받은 데이터를 get로 쿼리를 가져와라
                    request.data.get("rooms"),
                    request.data.get("toilets"),
                )
                if price:  # 예외처리문으로 해당 값이 음수라면 에러를 띄우는 조건문
                    if int(price) < 0:
                        raise ParseError("price 가 음수입니다.")
                if rooms:
                    if int(rooms) < 0:
                        raise ParseError("rooms 가 음수입니다.")
                if toilets:
                    if int(toilets) < 0:
                        raise ParseError("toileds 가 음수입니다.")

                category_pk = request.data.get("category")

                if category_pk:  # 카테고리의 아이디값을 받는다면
                    try:
                        category = Category.objects.get(pk=category_pk)
                    except Category.DoesNotExist:
                        raise ParseError("카테고리 값이 없자나~")
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("'rooms'가 아니자나~ ")
                    room.category = category

                amenities_pk = request.data.get("amenities")

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

            updated_room = serializer.save()
            return Response(
                RoomDetailSerializer(
                    updated_room,
                    context={"request": request},
                ).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)

        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # get 빼고 post, put, delete 모두 authenticated가 필요하다.

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)  # ,뒤는 기본값.
            page = int(page)  # 페이지 값을 무조건 int로 변환
        except ValueError:
            page = 1  # 실패시(문자열,문자,배열 등)
        page_size = settings.PAGE_SIZE  # 나눠질 페이지 단위
        start = (page - 1) * page_size
        end = start + page_size  # limiting query sets
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE

        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
