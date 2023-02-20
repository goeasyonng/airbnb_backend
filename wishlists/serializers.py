from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSeializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSeializer(
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
