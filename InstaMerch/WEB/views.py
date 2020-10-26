from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home_view(request):
    context = {
        "user": request.user
    }
    return render(request, 'WEB/home.html', context)


def purchase_view(request):
    return render(request, 'WEB/purchase.html')
