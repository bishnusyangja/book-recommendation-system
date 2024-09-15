from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'description', 'published_on', 'created_on', 'modified_on')