from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()  # 미래 날짜가 아닐때 반환하도록
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Check-in date must be in the future")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Check-out date must be in the future")
        return value

    def validate(self, data):
        if data["check_out"] < data["check_in"]:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        if Booking.objects.filter(
            check_in__lte=data["check_out"],  # lte작거나 같다
            check_out__gte=data["check_in"],  # gte크거나 같다
        ).exists():
            raise serializers.ValidationError("those dates are occupied")
        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
