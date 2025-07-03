from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.shortcuts import redirect, get_object_or_404, render
from .models import Product, Order, OrderItem, Recipe, RecipeStep
# Create your views here.

def thankyou(request):
    suggested_products = Product.objects.all()[:4]  # Gợi ý 4 sản phẩm bất kỳ

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        cartItems = 0
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub=False)

    context = {
        'suggested_products': suggested_products,
        'categories': categories,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, 'dopamine/thankyou.html', context)


def detail(request, id):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    # Lấy duy nhất một sản phẩm theo ID
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.filter(is_sub=False)

    context = {
        'categories': categories,
        'product': product,  # dùng product (không phải products nữa)
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'dopamine/detail.html', context)

def category(request):
    categories = Category.objects.filter(is_sub =False)
    customer = request.user
    order, created = Order.objects.get_or_create(customer =customer,complete =False)
    cartItems = order.get_cart_items
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categories, 'products':products, 'cartItems':cartItems, 'active_category':category}
    return render(request, 'dopamine/category.html',context)
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request, 'dopamine/search.html',{"searched":searched,"keys": keys,'products': products, 'cartItems':cartItems})
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'dopamine/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username =username, password =password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request, 'user or password not correct!')
    context = {}
    return render(request, 'dopamine/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    recipes = Recipe.objects.all()  # Lấy danh sách công thức
    context = {
        'recipes': recipes,
        # Các dữ liệu khác
    }
    categories = Category.objects.filter(is_sub =False)
    products = Product.objects.all()
    context= {'categories':categories,'products': products, 'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'dopamine/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub =False)
    context= {'categories':categories,'items':items, 'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'dopamine/cart.html', context)

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        customer = request.user
        product = get_object_or_404(Product, id=product_id)
        # Lấy hoặc tạo đơn hàng chưa hoàn thành của người dùng
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Lấy hoặc tạo sản phẩm trong đơn hàng
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        # Tăng số lượng sản phẩm
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')  # Chuyển hướng sang trang giỏ hàng

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.items.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context= {'items':items, 'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order.payment_method = payment_method
        order.complete = True
        order.save()
        return redirect('thankyou')  # Hoặc trang hoàn tất
    return render(request,'dopamine/checkout.html', context)
def process_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        payment_method = request.POST.get('payment_method')
        phone = request.POST.get('phone')
        # Cập nhật order
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.payment_method = payment_method
        order.complete = True
        order.save()

        # Lưu địa chỉ giao hàng
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            phone=phone,
        )

        return redirect('thankyou')  # bạn có thể tạo view tên thankyou

    return redirect('home')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
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

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    detailed_steps = RecipeStep.objects.filter(recipe=recipe)

    # Tách bước hướng dẫn thành danh sách
    steps_list = []
    for line in recipe.steps.split('\n'):
        if line.startswith('Bước'):
            steps_list.append(f"<strong>{line}</strong>")
        else:
            steps_list.append(line)

    # Tách và phân loại nguyên liệu
    ingredients_lines = recipe.ingredients.split('\n')
    parsed_ingredients = []
    seen = set()

    for line in ingredients_lines:
        line = line.strip()
        if not line or line in seen:
            continue
        seen.add(line)

    # Nếu dòng bắt đầu bằng số → là item
        if line[0].isdigit():
            parsed_ingredients.append({'type': 'item', 'content': line})
    # Nếu chữ đầu viết hoa và không bắt đầu bằng số → là header
        elif line[0].isalpha() and line[0].isupper():
            parsed_ingredients.append({'type': 'header', 'content': line})
        else:
            parsed_ingredients.append({'type': 'item', 'content': line})

    context = {
        'recipe': recipe,
        'steps_list': steps_list,
        'detailed_steps': detailed_steps,
        'parsed_ingredients': parsed_ingredients,
    }
    return render(request, 'dopamine/recipe_detail.html', context)

def all_recipes(request):
    recipe_type = request.GET.get('type', '')  # Lấy loại món ăn từ query parameters
    if recipe_type:
        recipes = Recipe.objects.filter(type=recipe_type)
    else:
        recipes = Recipe.objects.all()
    return render(request, 'dopamine/all_recipes.html', {'recipes': recipes})

