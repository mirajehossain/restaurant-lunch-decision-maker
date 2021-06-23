from rest_framework import serializers
from django.forms.models import model_to_dict
from rest_framework.validators import UniqueTogetherValidator

from base.validators import NonNegative
from item.models import Item
from item.models import MenuHours
from restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['slug', 'name', 'logo']


class ItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    price = serializers.FloatField(validators=[NonNegative("Price")], required=False)
    menu_hours = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def get_restaurant(self, obj):
        return RestaurantSerializer(obj.restaurant).data

    def get_menu_hours(self, obj):
        return MenuHoursLiteSerializer(obj.menu_hours, many=True).data


class AdminItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    price = serializers.FloatField(validators=[NonNegative("Price")], required=False)

    class Meta:
        model = Item
        fields = '__all__'


class ItemLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'description',
            'image',
            'price',
            'status',
        )


class MenuHoursSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuHours
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=MenuHours.objects.all(),
                fields=['restaurant', 'name', 'week_day']
            )
        ]

    def to_representation(self, instance):
        result = model_to_dict(instance)
        result['start_time'] = str(instance.start_time)
        result['end_time'] = str(instance.end_time)
        result['restaurant'] = RestaurantSerializer(instance.restaurant).data

        return result

    def to_internal_value(self, data):
        data['restaurant'] = Restaurant.objects.get(pk=data['restaurant'])

        return data


class MenuHoursLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuHours
        exclude = ('restaurant', 'created_by', 'updated_by', 'created_at', 'updated_at', 'status')
