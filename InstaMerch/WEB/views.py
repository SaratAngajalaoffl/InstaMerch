from django.shortcuts import render
from django.http import HttpResponse
import API.models as models
# Create your views here.


def home_view(request):

    context = {
        "user": request.user,
        "designs": models.Design.objects.all()
    }
    return render(request, 'WEB/home.html', context)


def purchase_view(request):
    return render(request, 'WEB/purchase.html')
