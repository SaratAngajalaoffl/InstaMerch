from .models import Designer, Design, Address, Order
from rest_framework import serializers


class Designer_serializer(serializers.ModelSerializer):

    class Meta:
        model = Designer
        fields = '__all__'


class Design_serializer(serializers.ModelSerializer):

    designer = serializers.ReadOnlyField(source='designer.user.username')
    picture_url = serializers.CharField(source='picture.url')

    class Meta:
        model = Design
        fields = ['price', 'picture_url', 'id', 'designer', 'category']


class Address_serializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class Orders_serializer(serializers.ModelSerializer):

    design_id = serializers.CharField(source='product')
    price = serializers.IntegerField(source='product.price')
    designer = serializers.CharField(source='product.designer.user.username')
    placed_on = serializers.CharField(source='created_at')
    # address = Address_serializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'design_id', 'status',
                  'price', 'designer', 'placed_on', 'expected_date', 'delivery_address']
        depth = 1
