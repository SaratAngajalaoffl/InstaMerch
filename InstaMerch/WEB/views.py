from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import WEB.forms as forms
import API.models as models


def home_view(request):

    context = {
        "user": request.user,
        "designs": models.Design.objects.all()
    }
    return render(request, 'WEB/home.html', context)


def purchase_view(request):
    return render(request, 'WEB/purchase.html')


def register_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

    context = {'form': form}

    return render(request, 'registration/register.html', context)
