from rest_framework import serializers
from .models import *


class ProductSerialier(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Product
        fields = '__all__'


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
