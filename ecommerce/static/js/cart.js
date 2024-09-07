var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action    = this.dataset.action
        console.log('productId:', productId, 'action:',action)
        console.log('User:', user)

        if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
            console.log('User is loged in')
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){

    var url = '/updateItem/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrfToken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('DATE: ', data)
        location.reload()
    })
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')
    
    // increase
	if (action == 'add'){
		if (cart[productId] == undefined){
		    cart[productId] = {'quantity':1}
		}else{
			cart[productId]['quantity'] += 1
		}
	}

    // decrease
	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}

    // update the cart
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}

// define the cart
var cart = JSON.parse(getCookie('cart'))

// if undefined cart creat new one 
if (cart == undefined){
    cart = {}
    console.log('Cart Created!', cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

console.log('Cart:', cart)
// using jQuery
// $(document).ready(function() {
//     $(document).on('click', '.update-cart', function() {
//         var productId = $(this).data('product');
//         var action = $(this).data('action');
//         console.log('productId:', productId, 'action:', action);
//     });
// });