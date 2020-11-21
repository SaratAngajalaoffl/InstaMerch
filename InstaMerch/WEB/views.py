from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import WEB.forms as forms
import API.models as models
import WEB.models as web_models
import datetime
import stripe

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

    bestsellers = sorted(designs,key = lambda design:design.purchases)[::-1][:6]

    context = {
        "user": request.user,
        'featured': featured[:6],
        'recent': recent[:6],
        'bestsellers':bestsellers
    }

    return render(request, 'WEB/home.html', context)


def purchase_view(request,designid):

    if request.method == 'POST':
        data = request.POST

        stripe.api_key = settings.STRIPE_SECRET_KEY

        product = models.Design.objects.get(id=designid)
        address = models.Address.objects.get(id=data['address'])
        
        items = [
            {
                    'name': product.title,
                    'quantity': data['qty'],
                    'currency': 'inr',
                    'amount': product.category.price,
            }
        ]
        
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url="http://localhost:8000/orders",
                cancel_url="http://localhost:8000/orders",
                payment_method_types=['card'],
                mode='payment',
                line_items=items
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})
            
        order = models.Order(address=address)
        
        if 'account' in data['address']:
            order.account = address.account

        order.save()
        order.products.set([product])
        order.session_id = checkout_session['id']
        order.save()

        context = {
            "session_id" : checkout_session.id
        }    

        return render(request,'WEB/stripe_redirect.html',context)
        
    context = {
        'addresses':request.user.account.address_set.all(),
        'designid':designid
    }
    return render(request, 'WEB/purchase.html',context)


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
            return redirect('add_profile_pic')

    context = {'form': form}

    return render(request, 'registration/register.html', context)


def design_view(request, designid):
    design = models.Design.objects.get(id=designid)
    context = {
        'design': design
    }
    return render(request, 'WEB/design_detail.html', context)


@login_required(login_url='/accounts/login')
def add_profile_pic(request):
    if request.method == 'POST':
        data = request.FILES
        account = models.Account.objects.get(user = request.user)
        account.picture = data['profilepic']
        account.save()
        return redirect('dashboard')
    return render(request,'WEB/add_profile_picture.html')

@login_required(login_url='/accounts/login')
def post_design_view(request):
    if request.method == 'POST':
        data = request.POST
        picture = request.FILES

        design = models.Design(
            title = data['title'],
            picture = picture['designpic'],
            category = models.Category.objects.get(name = data['category']),
            account = request.user.account
        )
        design.save()
        return redirect('home')
    categories = models.Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'WEB/post_design.html',context)

@login_required(login_url='accounts/login')
def show_cart_view(request):
    cart = web_models.Cart.objects.get(account=request.user.account)
    cart_items = cart.item.all()

    total = 0

    for item in cart_items:
        total += item.category.price
    
    context = {
        'items':cart_items,
        'total':total
    }

    return render(request,'WEB/cart.html',context)

@login_required(login_url='accounts/login')
def add_to_cart_view(request,designid):
    design = models.Design.objects.get(id=designid)
    cart = web_models.Cart.objects.get(account=request.user.account)

    if design not in cart.item.all():
        cart.item.add(design)
        cart.save()
        return redirect('cart')
    else:
        return HttpResponse("<h1>Design Already in Cart</h1>")

@login_required(login_url='accounts/login')
def remove_from_cart_view(request,designid):
    design = models.Design.objects.get(id=designid)
    cart = web_models.Cart.objects.get(account=request.user.account)

    if design in cart.item.all():
        cart.item.remove(design)
        return redirect('cart')
    else:
        return HttpResponse("<h1>Item not in Cart</h1>")

@login_required(login_url='accounts/login')
def dashboard_view(request):
    return render(request,'WEB/dashboard.html')

@login_required(login_url='accounts/login')
def orders_view(request):
    return render(request,'WEB/orders.html')

@login_required(login_url='accounts/login')
def manage_addresses_view(request):    
    context = {
        'addresses':request.user.account.address_set.all()
    }
    return render(request,'WEB/addresses.html',context)

@login_required(login_url='accounts/login')
def designs_view(request):
    designs = request.user.account.design_set.all()
    context = {
        'designs':designs
    }
    return render(request,'WEB/designs.html',context)

@login_required(login_url='accounts/login')
def delete_design_view(request,designid):
    design = models.Design.objects.get(id=designid)

    if design.account == request.user.account:
        design.delete()
        return redirect('my-designs')
    return render(request,'WEB/designs.html',context)

@login_required(login_url='accounts/login')
def settings_view(request):
    context = {}
    return render(request,'WEB/account-settings.html',context)


@login_required(login_url='accounts/login')
def add_address_view(request):

    if request.method == 'POST':
        data = request.POST

        address = models.Address(
            name = data['name'],
            address_line1 = data['address_line1'],
            address_line2 = data['address_line2'],
            state = data['state'],
            city = data['city'],
            country = data['country'],
            pincode = data['pincode'],
            telephone = data['telephone'],
            account = request.user.account
        )
        address.save()
        return redirect('manage-addresses')
    
    context = {}
    return render(request,'WEB/add_address.html',context)