from users.serializers import UserSerializer
from rest_framework.generics import CreateAPIView


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer


