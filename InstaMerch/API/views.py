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
def api_post_order(request):

    data = request.data
    address = models.Address(
        address_line1 = data['address']["address_line1"],
        address_line2 = data['address']["address_line2"],
        state = data['address']["state"],
        city = data['address']["city"],
        country = data['address']["country"],
        pincode = data['address']["pincode"]
    )
    address.save()
    if 'account' in data['address']:
        address.account = models.Account.objects.get(id =data['address']["account"])
        address.save()
    products = []
    for product in data['products']:
        products.append(models.Design.objects.get(id=product["product_id"]))
    items = []
    for i,product in enumerate(products):
        product.purchases += data['products'][i]["qty"]
        product.save()
        item = {
                    'name': product.category.name,
                    'quantity': data['products'][i]["qty"],
                    'currency': 'inr',
                    'amount': product.category.price,
                }
        items.append(item)

    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=data['success_url'],
            cancel_url=data['cancelled_url'],
            payment_method_types=['card'],
            mode='payment',
            line_items=items
        )
    except Exception as e:
        return JsonResponse({'error': str(e)})

    order = models.Order(address=address)
    order.save()
    order.products.set(products)
    order.session_id = checkout_session['id']
    order.save()
    serializer = serializers.Orders_serializer(order)
    # serializer = serializers.Orders_serializer(
    #     order, data={"session_id": })
    # if serializer.is_valid():
    #     serializer.save()

    return Response(serializer.data)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        order = models.Order.objects.get(
            session_id=event['data']['object']['id'])
        order.status = "Payment Confirmed"
        order.save()

    return HttpResponse(status=200)
