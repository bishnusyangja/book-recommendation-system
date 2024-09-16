from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'email', 'mobile', 'is_active', 'created_on', 'modified_on',
                  'password', 'confirm_password', )

    def validate(self, attrs):
        passwd = attrs.get('password')
        confirm_passwd = attrs.get('confirm_password')
        if not passwd or passwd != confirm_passwd:
            raise serializers.ValidationError({'password': 'password confirmation doesnot match'})
        return attrs


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
