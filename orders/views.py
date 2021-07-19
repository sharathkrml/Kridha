from accounts.models import Addresses, CustomUser
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, Order, Wishlist
from products.models import Product
# Create your views here.
from django.urls import reverse
from products.views import NavBar, product
from products.models import Category
navbar = NavBar(Category)


@csrf_exempt
def addtocart(request):
    if request.method == 'POST':
        print(request.POST)
        user = request.user
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)
        quantity = request.POST['quantity']
        if(len(Cart.objects.filter(product_id=product, user_id=user, ordered=False)) == 0):
            # checks if there is an entry,if no
            new = Cart(user_id=user, product_id=product,
                       quantity=int(quantity), ordered=False)
            new.save()
        else:
            old_entry = Cart.objects.filter(
                product_id=product, user_id=user).filter(ordered=False).first()
            old_entry.quantity = old_entry.quantity + int(quantity)
            old_entry.save()

    return HttpResponse(status=200)


@csrf_exempt
def getcart(request):
    if(request.method == 'POST'):
        if(request.POST.get('delete_id')):
            cart_object = Cart.objects.get(pk=request.POST['delete_id'])
            cart_object.delete()
        elif(request.POST.get('change_id')):
            cart_object = Cart.objects.get(pk=request.POST['change_id'])
            cart_object.quantity = request.POST['quantity']
            cart_object.save()
    cart_products = Cart.objects.filter(
        user_id=request.user).filter(ordered=False)
    print(cart_products)
    cart_dict = {}
    j = 0
    total = 0
    for i in cart_products:
        j = j+1
        d = {}
        d['cart_id'] = i.id
        d['product_name'] = i.product_id.productname
        d['product_url'] = reverse('product_url') + i.product_id.slug
        d['selling_price'] = i.product_id.selling_price
        d['quantity'] = i.quantity
        d['image'] = i.product_id.image[1:-
                                        1].replace("'", '').replace(" ", '').split(',')[0]
        d['product_total'] = i.product_id.selling_price * \
            i.quantity
        cart_dict[j] = d
        total = total + i.product_id.selling_price * i.quantity
    j = 0
    cart_dict['total'] = total
    return JsonResponse(cart_dict)


@csrf_exempt
def cart(request):
    return render(request, 'Orders/cart.html', {'title': 'Cart', 'navbar': navbar.details()})


@csrf_exempt
def checkout(request):
    if(request.method == 'POST'):
        address_id = request.POST.get('address_id')
        address = Addresses.objects.get(pk=address_id)
        cart = Cart.objects.filter(
            user_id=request.user, ordered=False)
        total = 0
        for i in cart:
            total = total+i.cart_total_price
        order = Order(
            user_id=request.user,
            address_id=address,
            delivery_status='YET TO BE DISPATCHED',
            total_price=total
        )
        order.save()
        order.cart_ids.set(cart)
        print(order)
        for i in cart:
            i.ordered = True
            i.save()
        return JsonResponse({'success': True})
    addresses = Addresses.objects.filter(user_id=request.user.id)
    return render(request, 'Orders/checkout.html', {'title': 'Checkout', 'addresses': addresses, 'navbar': navbar.details()})


@csrf_exempt
def address(request):
    if(request.method == 'POST'):
        print(request.POST)
        address = Addresses(
            user_id=request.user,
            fullname=request.POST.get('fullname'),
            mobile_no=request.POST.get('mobile_no'),
            pin_code=request.POST.get('pin_code'),
            building_details=request.POST.get('building_details'),
            area_details=request.POST.get('area_details'),
            landmark_details=request.POST.get('landmark_details'),
            town_details=request.POST.get('town_details'),
            state=request.POST.get('state'),
            address_type=request.POST.get('address_type'),
        )
        address.save()
    return HttpResponse(status=200)


def getorder(request):
    orders = Order.objects.filter(user_id=request.user)
    orders_dict = {}
    ord_count = 0
    for order in orders:
        ord_count = ord_count+1
        product_name = []
        order_id = order.id
        total_price = order.total_price
        for cart in order.cart_ids.all():
            product_name.append(cart.product_id.productname)
        orders_dict[ord_count] = {
            'product_name': product_name, 'order_id': order_id, 'total_price': total_price}

    print(orders_dict)
    return JsonResponse(orders_dict)


@csrf_exempt
def wishlist(request):
    if(request.method == 'POST'):
        if(request.POST.get('delete_id')):
            wishlist_delete = Wishlist.objects.get(
                pk=request.POST['delete_id'])
            wishlist_delete.delete()
        if(request.POST.get('add_id')):
            cart_add = Wishlist.objects.get(
                pk=request.POST['add_id'])
            cart_obj = Cart(product_id=cart_add.product_id,
                            user_id=cart_add.user_id,
                            quantity=1,
                            ordered=False
                            )
            cart_obj.save()
            cart_add.delete()
        wishlist = Wishlist.objects.filter(user_id=request.user)
        wish_dict = {}
        count = 0
        for i in wishlist:
            count = count+1
            prod_name = i.product_id.productname
            prod_image = i.product_id.image[1:-
                                            1].replace("'", '').replace(" ", '').split(',')[0]
            product_url = reverse('product_url') + i.product_id.slug

            prod_price = i.product_id.selling_price
            wishlist_id = i.id
            wish_dict[count] = {
                'wishlist_id': wishlist_id, 'product_url': product_url, 'prod_name': prod_name, 'prod_image': prod_image, 'prod_price': prod_price}
        return JsonResponse(wish_dict)
    return render(request, 'Orders/wishlist.html', {'title': 'Wishlist', 'navbar': navbar.details()})
