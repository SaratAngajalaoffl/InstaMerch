from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import WEB.forms as forms
import API.models as models
import WEB.models as web_models
import datetime

def home_view(request):

    designs = models.Design.objects.all()
    featured = []
    recent = []

    for design in designs:
        if design.isfeatured:
            featured.append(design)
        timedelta = design.createdon - datetime.date.today()
        if timedelta.days < 10:
            recent.append(design)
        
        if len(recent) == 6:
            break 

    bestsellers = sorted(designs,key = lambda design:design.purchases)[::-1][:6]

    context = {
        "user": request.user,
        'featured': featured,
        'recent': recent,
        'bestsellers':bestsellers
    }

    return render(request, 'WEB/home.html', context)


def purchase_view(request):
    return render(request, 'WEB/purchase.html')


def register_view(request):
    form = forms.CreateUserForm()

    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            account = models.Account(user = user)
            cart = web_models.Cart(account = account)
            account.save()
            cart.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}

    return render(request, 'registration/register.html', context)


def design_view(request, designid):
    design = models.Design.objects.get(id=designid)
    context = {
        'design': design
    }
    return render(request, 'WEB/design_detail.html', context)
