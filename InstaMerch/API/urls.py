from django.urls import path
from django.views.decorators.csrf import csrf_exempt

import API.views as views

urlpatterns = [
    path('<str:orgname>/designs', views.api_org_get_designs, name="get_designs"),
    path('orders/<str:orderid>', views.api_get_order_status, name="order_status"),
    path('place-order/', csrf_exempt(views.api_post_order), name="post_order"),
    path('config/', views.stripe_config),
    path('webhook/', views.stripe_webhook),
]
