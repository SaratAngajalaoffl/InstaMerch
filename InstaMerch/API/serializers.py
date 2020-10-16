from .models import Designer, Design, Address, Order
from rest_framework import serializers


class Designer_serializer(serializers.ModelSerializer):

    class Meta:
        model = Designer
        fields = '__all__'


class Design_serializer(serializers.ModelSerializer):

    class Meta:
        model = Design
        fields = '__all__'


class Address_serializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class Orders_serializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
