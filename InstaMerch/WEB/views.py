from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import WEB.forms as forms
import API.models as models
import WEB.models as web_models
from django.contrib.auth.models import User
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

@login_required(login_url='/accounts/login')
def cart_checkout_view(request,addressid):

    cart_items = request.user.account.cart.item.all()

    stripe.api_key = settings.STRIPE_SECRET_KEY

    address = models.Address.objects.get(id=addressid)
    
    items = []
    
    for item in cart_items:
        items.append({
            'name': item.title,
            'quantity': 1,
            'currency': 'inr',
            'amount': item.category.price,
        })
    
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

    request.user.account.cart.item.clear()
    
    order.account = address.account

    order.save()
    order.products.set(cart_items)
    order.session_id = checkout_session['id']
    order.save()

    context = {
        "session_id" : checkout_session.id
    }    

    return render(request,'WEB/stripe_redirect.html',context)


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
    addresses = request.user.account.address_set.all()

    total = 0

    for item in cart_items:
        total += item.category.price
    
    context = {
        'items':cart_items,
        'total':total,
        'addresses':addresses
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

    orders = request.user.account.order_set.all()
    
    context = {
        'orders':orders
    }
    
    return render(request,'WEB/orders.html',context)

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

def user_designs_view(request,username):

    if request.user.is_authenticated:
        if request.user.username == username:
            return redirect('my-designs')
    
    user = User.objects.get(username=username)
    account = models.Account.objects.get(user=user)

    context = {
        'user': account,
        'designs':account.design_set.all()
    }

    return render(request,"WEB/user_designs.html",context)

def designs_by_category_view(request,categoryid):
    category = models.Category.objects.get(id=categoryid)

    context = {
        'designs':category.design_set.all(),
        'category':category.name
    }

    return render(request,'WEB/designs_of_category.html',context)

def delete_account_view(request):
    user = request.user
    user.delete()

    return redirect('home')

def update_password_view(request):

    if request.method == 'POST':
        data = request.POST

        if data['password1'] == data['password2']:
            request.user.set_password(data['password1'])
            request.user.save()
            return redirect('login')
        else:
            return HttpResponse('Passwords Donot Match')
    
    return render(request,"WEB/password_change.html")

def search_view(request):

    if request.method == 'POST':

        data = request.POST

        users = User.objects.filter(username__trigram_similar=data['search-key'])
        design_set = models.Design.objects.filter(title__trigram_similar=data['search-key'])
        categories = models.Category.objects.filter(name__trigram_similar=data['search-key'])

        designs = []

        for category in categories:
            for design in category.design_set.all():
                designs.append(design)

        for design in design_set:
            if design not in designs:
                designs.append(design)
        
        print("Designs are",designs)
        

        context = {
            'users':users,
            'designs':designs
        }

        return render(request,"WEB/searchresults.html",context)