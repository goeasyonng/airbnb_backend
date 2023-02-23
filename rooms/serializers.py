from rest_framework.serializers import ModelSerializer  # 시리얼라이즈 코드를 사용하기 위한 import
from rest_framework import serializers
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from .models import Amenity, Room
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        else:
            return false

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            room__pk=room.pk,
        ).exists()


class RoomListSeializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
        # depth = 1  # 해당 id값을 가진 모델의 속성들이 나타난다(관계성을 확장한다), 커스텀이 불가하다

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
