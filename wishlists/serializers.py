from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSeializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):

    room = RoomListSeializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
