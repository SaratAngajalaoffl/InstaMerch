import API.models as models
from rest_framework import serializers


class Design_serializer(serializers.ModelSerializer):

    account = serializers.CharField(source='account.user.username')

    class Meta:
        model = models.Design
        fields = ['id', 'picture', 'account', 'category']
        depth = 1


class Orders_serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'products', 'placed_on','status', 'address', 'session_id']
        depth = 2
