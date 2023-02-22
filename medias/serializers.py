from rest_framework.serializers import ModelSerializer
from .models import Photo


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )

    # def cerate(self, validated_data):
    #     return super().create(validated_data)
