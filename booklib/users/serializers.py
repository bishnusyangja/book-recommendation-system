from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'mobile', 'is_active', 'created_on', 'modified_on',
                  'password', 'confirm_password', )

    def validate(self, attrs):
        passwd = self.attrs.get('password')
        confirm_passwd = self.attrs.get('confirm_password')
        if not passwd or passwd != confirm_passwd:
            raise serializers.ValidationError({'password': 'password confirmation doesnot match'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
