from rest_framework import serializers

from user.models import User


class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'address', 'first_name', 'last_name', 'profile_pic_url')
