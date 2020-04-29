from django.shortcuts import render, redirect

# Create your views here.
# from django.http import HttpResponse
from .models import Product, Order, Customer
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users


def home(request):    
    return redirect('dashboard')

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()    
    return render(request, 'index.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context = {
        'orders' : orders, 
        'customers': customers, 
        'total_customers': total_customers, 
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    # if request.method == 'GET':

    context = {  'myFilter': myFilter, 'customer': customer, 'orders': orders, 'total_order': total_order }
    return render(request, 'customer.html', context)

@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':    
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = { 'form': form }
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = { 'form': form }
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, id):
    order = Order.objects.get(id= id)
    context = {'order': order}
    if request.method == "POST":
        order.delete()
        return redirect('/dashboard')
    return render(request, 'delete.html', context)

@unauthenticated_user
def register(request):
    form  = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.cleaned_data.get('username')
            messages.success(request, 'Created ' + user)
            form.save()

    context = { 'form': form }
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else: 
            messages.info(request, 'User or pass is not correct')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

import json

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    userId = str(request.user.customer.id)
    print(userId)
    return redirect('/customer/' + userId)