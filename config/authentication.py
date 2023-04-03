from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.headers.get("Trust-Me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)  # 규칙임. user 먼저 나오고 None이 나오는 튜플 반환해야함
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user{username}")
