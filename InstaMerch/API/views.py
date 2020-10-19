from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import API.models as models
import API.serializers as serializers
import stripe


@api_view(['GET'])
def api_org_get_designs(request, orgname):
    org = User.objects.get(username=orgname)
    account = models.Account.objects.get(user=org)
    designs = models.Design.objects.filter(account=account)
    serializer = serializers.Design_serializer(designs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_get_order_status(request, orderid):
    try:
        order = models.Order.objects.get(id=orderid)
        serializer = serializers.Orders_serializer(order)
        return Response(serializer.data)
    except:
        return HttpResponse("No order with order id " + str(orderid) + "found.")


@api_view(['POST'])
def api_post_order_status(request):

    data = request.data
    address = models.Address.objects.get(id=data['address'])
    product = models.Design.objects.get(id=data['product'])

    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=data['success_url'],
            cancel_url=data['cancelled_url'],
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'name': product.category.name,
                    'quantity': data['quantity'],
                    'currency': 'inr',
                    'amount': product.category.price,
                },
            ]
        )
    except Exception as e:
        return JsonResponse({'error': str(e)})

    order = models.Order(address=address, product=product)

    serializer = serializers.Orders_serializer(
        order, data={"session_id": checkout_session['id']})
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
