from django.urls import path

from .views import api_org_get_designs, api_get_order_status

urlpatterns = [
    path('<str:orgid>/designs', api_org_get_designs, name="get_designs"),
    path('orders/<str:orderid>', api_get_order_status, name="order_status")
]
