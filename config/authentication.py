from rest_framework.authentication import BaseAuthentiaction


class TrustMeBroAuthentication(BaseAuthentiaction):
    def authenticate(self, request):
        print(request.heasers)
        return None
