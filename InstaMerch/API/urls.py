from django.urls import path

from .views import api_org_get_designs

urlpatterns = [
    path('<str:orgid>/designs', api_org_get_designs, name="get_designs")
]
