from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import *

def store(request):
    cart = cartData(request)
    order = cart['order']
    items = cart['items']
    
    context = {
        'range': range(9),
        'products': Product.objects.all(),
        'items':items,
        'order':order,
    }
    return render(request, 'store/store.html', context)

def cart(request):

    cart = cartData(request)
    order = cart['order']
    items = cart['items']

    context = {
        'items':items,
        'order':order,
        }
    
    return render(request, 'store/cart.html', context)

def checkout(request):
    cart = cartData(request)
    order = cart['order']
    items = cart['items']
    print(order)
    context = {
        'items':items,
        'order':order,
        }
    return render(request, 'store/checkout.html', context)

# if authenticated user
def updateItem(request):
    # request data
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # check product in DB
    customer = request.user.customer
    product  = Product.objects.get(id=productId)

    # if customer not have order would create one {not completed order}
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # check for item itself in order
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.qty = orderItem.qty + 1
    elif action == 'remove':
        orderItem.qty = orderItem.qty - 1

    orderItem.save()

    if orderItem.qty <= 0:
        orderItem.delete()

    print(product)
    return JsonResponse('item was good', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if(request.user.is_authenticated):
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
     
    else:
        customer, order = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.status = 1 # Pending For Payment
    order.total = total
      
    if total == float(order.get_cart_total_price):
        order.complete = True

    order.save()    

    if order.should_shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order   = order,
            address = data['shipping']['address'],
            city    = data['shipping']['city'],
            state   = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete!', safe=False)
    