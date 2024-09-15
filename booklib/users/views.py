from users.models import User
from users.serializers import UserSerializer
from rest_framework.generics import CreateAPIView


class UserRegisterAPIView(CreateAPIView):
    # permission_classes = ( default permission is allowAny from settings )
    serializer_class = UserSerializer


