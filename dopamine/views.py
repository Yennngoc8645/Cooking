from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'dopamine/register.html',context)
def login(request):
    context = {}
    return render(request, 'dopamine/login.html',context)
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context= {'products': products, 'cartItems':cartItems}
    return render(request,'dopamine/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items

    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context= {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'dopamine/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items

    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context= {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'dopamine/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer =customer,complete =False)
    orderItem, created = OrderItem.objects.get_or_create(order =order,product =product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
# def updateItem(request):
#     try:
#         # Đọc dữ liệu từ request
#         data = json.loads(request.body)
#         productId = data.get('productId')
#         action = data.get('action')

#         if not productId or not action:
#             return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)

#         if not request.user.is_authenticated:
#             return JsonResponse({'error': 'Người dùng chưa đăng nhập'}, status=403)

#         customer = request.user.customer
#         product = Product.objects.get(id=productId)

#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

#         if action == 'add':
#             orderItem.quantity += 1
#         elif action == 'remove':
#             orderItem.quantity -= 1

#         orderItem.save()

#         if orderItem.quantity <= 0:
#             orderItem.delete()

#         return JsonResponse({'message': 'Cập nhật thành công'}, safe=False)

#     except Product.DoesNotExist:
#         return JsonResponse({'error': 'Sản phẩm không tồn tại'}, status=404)
#     except Exception as e:
#         print(f"Lỗi server: {e}")  # Log lỗi chi tiết
#         return JsonResponse({'error': 'Đã xảy ra lỗi trên server'}, status=500)

