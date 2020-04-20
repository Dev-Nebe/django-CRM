from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *
from accounts.forms import OrderForm


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_number_customers = customers.count()

    total_number_orders = orders.count()

    orders_delivered = orders.filter(status='Delivered').count()

    orders_pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_number_customers': total_number_customers,
        'total_number_orders': total_number_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    orders = customer.order_set.all()

    total_orders = orders.count()

    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders}

    return render(request, 'accounts/customer.html', context)


def createOrder(request):
    form = OrderForm()

    context = {
        'form': form
    }

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, order_id):
    order = Order.objects.get(id=order_id)

    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, order_id):

    order = Order.objects.get(id=order_id)

    context = {
        'order': order
    }

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete_order.html', context)
