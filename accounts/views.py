from django.shortcuts import render, redirect

# Create your views here.
# from django.http import HttpResponse
from .models import Product, Order, Customer
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
    products = Product.objects.all()    
    return render(request, 'index.html', {'products': products})
    # return HttpResponse("home page")

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

def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = OrderFilter()

    context = {  'myFilter': myFilter, 'customer': customer, 'orders': orders, 'total_order': total_order }
    return render(request, 'customer.html', context)

def createOrder(request):
    form = OrderForm()
    print("form hi")
    if request.method == 'POST':
        print("Printing POST: ", request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = { 'form': form }
    return render(request, 'order_form.html', context)

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

def deleteOrder(request, id):
    order = Order.objects.get(id= id)
    context = {'order': order}
    if request.method == "POST":
        order.delete()
        return redirect('/dashboard')
    return render(request, 'delete.html', context)