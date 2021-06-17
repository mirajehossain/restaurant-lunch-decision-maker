from rest_framework import serializers

from restaurant.models import Restaurant
from user.serializers import UserLiteSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_owner(self, obj):
        return UserLiteSerializer(obj.owner).data


class RestaurantLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'slug',
            'address',
            'logo',
        )
