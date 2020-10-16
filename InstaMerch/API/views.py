from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Designer, Design
from .serializers import Design_serializer, Designer_serializer, Address_serializer, Orders_serializer


@api_view(['GET'])
def api_org_get_designs(request, orgid):
    org = User.objects.get(username=orgid)
    designer = Designer.objects.get(user=org)
    design = Design.objects.get(designer=designer)
    serializer = Design_serializer(design)
    return Response(serializer.data)
