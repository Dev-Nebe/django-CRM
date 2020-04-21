from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from accounts.models import *
from accounts.forms import OrderForm
from accounts.filters import OrderFilter


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

    # This next line uses the order filter to filter the 'orders' queryset based on the parameters of the GET request to which is handled by this view
    my_filter = OrderFilter(request.GET, queryset=orders)

    # This next line returns a filtered version of the 'orders' query set (qs)
    orders = my_filter.qs

    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders, 'my_filter': my_filter}

    return render(request, 'accounts/customer.html', context)


def createOrder(request, customer_id):

    order_formset = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=4)

    customer = Customer.objects.get(id=customer_id)

    formset = order_formset(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={'customer': customer})

    context = {
        'formset': formset
    }

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = order_formset(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
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
