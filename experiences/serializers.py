from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        exclude = ("created_at", "updated_at")

    def validate(self, data):
        if data.get("start") or data.get("end"):
            if data.get("start") and data.get("end"):
                if data["start"] >= data["end"]:
                    raise serializers.ValidationError(
                        "Start date must be before end date"
                    )
                else:
                    return data
            else:
                raise serializers.ValidationError(
                    "you must provide start and end dates"
                )
        else:
            return data
