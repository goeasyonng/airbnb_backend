from rest_framework.serializers import ModelSerializer
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    host = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        exclude = ("created_at", "updated_at")
