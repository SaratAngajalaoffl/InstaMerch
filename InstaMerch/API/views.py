from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Designer, Design, Order
from .serializers import Design_serializer, Designer_serializer, Address_serializer, Orders_serializer


@api_view(['GET'])
def api_org_get_designs(request, orgid):
    org = User.objects.get(username=orgid)
    designer = Designer.objects.get(user=org)
    designs = Design.objects.filter(designer=designer)
    serializer = Design_serializer(designs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_get_order_status(request, orderid):
    try:
        order = Order.objects.get(id=orderid)
        print("Order is ", order)
        serializer = Orders_serializer(order)
        return Response(serializer.data)
    except:
        return HttpResponse("No order with order id " + str(orderid) + "found.")
