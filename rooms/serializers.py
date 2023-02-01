from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    # def create(self, validated_data):
    #     print(validated_data)
    #     return


class RoomListSeializer(ModelSerializer):
    class Meta:
        model = Room
        # fields = "__all__"
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
        # depth = 1  # 해당 id값을 가진 모델의 속성들이 나타난다(관계성을 확장한다), 커스텀이 불가하다
