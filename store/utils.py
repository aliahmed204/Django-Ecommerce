import json
from .models import *
import datetime

def cookieCart(request):
    
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = []   

    items = []
    order = {'get_cart_total_qty':0, 'get_cart_total_price':0, 'should_shipping':False}
    cartItems = order['get_cart_total_price']
    
    for i in cart:
    #We use try block to prevent items in cart that may have been removed from causing error
        try:	
            if(cart[i]['quantity'] > 0): #items with negative quantity = lot of freebies  
                # cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total   = (product.price * cart[i]['quantity'])

                order['get_cart_total_qty']   += cart[i]['quantity']
                order['get_cart_total_price'] += total

                item = {
                    'id':product.id,
                    'product':{
                        'id': product.id,
                        'name': product.name,
                        'price': product.price, 
                        'imageURL': product.imageURL,
                        },
                    'qty': cart[i]['quantity'],
                    'is_digital': product.is_digital,
                    'get_total': total,
                }
                
                items.append(item)

                if product.is_digital == False:
                    order['should_shipping'] = True

        except Exception as e:
            print(f"An error occurred: {e}")

    return {'order':order, 'items':items}        

def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # customer has one order not completed
        items = order.orderitem_set.all()

    else:
        cartData = cookieCart(request)
        order = cartData['order']
        items = cartData['items']

    return {'order':order, 'items':items}  

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

    # check if email exict
	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			qty=(item['qty'] if item['qty'] > 0 else -1 * item['qty'] ), # negative quantity = freebies
		)
	return customer, order