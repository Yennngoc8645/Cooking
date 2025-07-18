# views.py - cleaned and checked for functionality

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from collections import defaultdict
from django.db.models import Sum, Count
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from dopamine.models import OrderItem, Order

def thong_ke_hang_ban(request):
    # --- Lấy tất cả OrderItem của đơn đã hoàn tất ---
    items = (
        OrderItem.objects
        .filter(order__complete=True)
        .select_related('product')
        .prefetch_related('product__category')   # vì Product.category là Many‑to‑Many
    )

    # ---------- Gom dữ liệu ----------
    product_stats  = defaultdict(lambda: {'tong_so_luong': 0, 'categories': set()})
    category_stats = defaultdict(int)   # {tên danh mục: tổng quantity}

    for item in items:
        product  = item.product
        quantity = item.quantity

        product_stats[product]['tong_so_luong'] += quantity

        cats = product.category.all()
        if not cats:
            cats = ['Khác']
        for cat in cats:
            cat_name = cat if isinstance(cat, str) else cat.name
            category_stats[cat_name] += quantity
            product_stats[product]['categories'].add(cat_name)

    # Danh sách theo sản phẩm, sắp xếp giảm dần số lượng
    thong_ke = sorted(product_stats.items(),
                      key=lambda x: x[1]['tong_so_luong'],
                      reverse=True)

    # ---------- KPI ----------
    tong_don_hang   = Order.objects.filter(complete=True).count()
    tong_san_pham   = sum(category_stats.values())
    danh_muc_ban_chay = max(category_stats, key=category_stats.get) if category_stats else '‑'
    san_pham_hot      = thong_ke[0][0].name if thong_ke else '‑'

    # ---------- Dữ liệu cho biểu đồ cột ----------
    labels = list(category_stats.keys())
    data   = [category_stats[label] for label in labels]

    # ---------- Trả về template ----------
    return render(request, 'dopamine/thong_ke.html', {
        'thong_ke': thong_ke,                    # bảng sản phẩm
        'labels':   json.dumps(labels),          # trục X biểu đồ
        'data':     json.dumps(data),            # giá trị cột

        # KPI
        'tong_don_hang':        tong_don_hang,
        'tong_san_pham':        tong_san_pham,
        'danh_muc_ban_chay':    danh_muc_ban_chay,
        'san_pham_hot':         san_pham_hot,
    })

def autocomplete_products(request):
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q:
        products = Product.objects.filter(name__istartswith=q)[:10]
        suggestions = [p.name for p in products]
    return JsonResponse({'results': suggestions})

def search(request):
    query = request.GET.get("q", "").strip()
    keys = Product.objects.filter(name__istartswith=query)

    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

    return render(request, 'dopamine/search.html', {
        "searched": query,
        "keys": keys,
        "cartItems": cartItems,
    })

def thankyou(request):
    suggested_products = Product.objects.all()[:4]

    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        cartItems = 0
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    context = {
        'suggested_products': suggested_products,
        'categories': categories,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, 'dopamine/thankyou.html', context)
def detail(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')

    # Gợi ý sản phẩm cùng danh mục
    if product.category.exists():
        related_products = Product.objects.filter(
            category__in=product.category.all()
        ).exclude(id=product.id).distinct()
    else:
        related_products = Product.objects.none()

    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cartItems = 0
    user_not_login = "show"
    user_login = "hidden"

    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.filter(product__isnull=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    context = {
        'categories': categories,
        'product': product,
        'related_products': related_products,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'dopamine/detail.html', context)

# views.py

def category(request):
    slug = request.GET.get('category', '')
    products = Product.objects.none()
    categories = Category.objects.filter(parent__isnull=True)
    cartItems = 0
    category_obj = None

    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

    if slug:
        category_obj = get_object_or_404(Category, slug=slug)
        if category_obj.children.exists():
            child_ids = category_obj.children.values_list('id', flat=True)
            products = Product.objects.filter(category__in=child_ids)
        else:
            products = Product.objects.filter(category=category_obj)

    return render(request, 'dopamine/category.html', {
        'categories': categories,
        'products': products,
        'cartItems': cartItems,
        'active_category': slug,
        'category_obj': category_obj,   # 👉 Thêm dòng này
    })

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'dopamine/register.html', {'form': form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tên người dùng hoặc mật khẩu không đúng!')
    return render(request, 'dopamine/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cartItems = 0
    user_not_login = "show"
    user_login = "hidden"

    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.filter(product__isnull=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    products = Product.objects.all()
    return render(request, 'dopamine/home.html', {
        'categories': categories,
        'products': products,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    })

def cart(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cartItems = 0
    user_not_login = "show"
    user_login = "hidden"

    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.filter(product__isnull=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'dopamine/cart.html', context)

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        customer = request.user
        product = get_object_or_404(Product, id=product_id)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, _ = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')

def checkout(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cartItems = 0
    user_not_login = "show"
    user_login = "hidden"

    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.filter(product__isnull=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')
            order.payment_method = payment_method
            order.save()  # lưu lại phương thức thanh toán

            if payment_method == 'momo':
                # Không đánh dấu complete ở đây → chờ xác nhận ở momo_payment
                return redirect('momo_payment', order_id=order.id)
            else:
                # COD hoặc các phương thức khác
                order.complete = True
                order.save()
                return redirect('thankyou')

    return render(request, 'dopamine/checkout.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    })
def chuan_hoa_danh_muc(name):
    name = name.lower()
    if 'cải' in name:
        return 'Cải'
    elif 'quả' in name:
        return 'Quả'
    elif 'củ' in name:
        return 'Củ'
    elif 'trứng' in name or 'sữa' in name:
        return 'Trứng sữa'
    return 'Khác'

def process_order(request):
    if request.method == 'POST':
        customer = request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        order.payment_method = request.POST.get('payment_method')
        order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            phone=request.POST.get('phone'),
        )

        return redirect('thankyou')
    return redirect('home')

def updateItem(request):
    data = json.loads(request.body)
    customer = request.user
    product = get_object_or_404(Product, id=data['productId'])
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, _ = OrderItem.objects.get_or_create(order=order, product=product)

    if data['action'] == 'add':
        orderItem.quantity += 1
    elif data['action'] == 'remove':
        orderItem.quantity -= 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('added', safe=False)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    detailed_steps = RecipeStep.objects.filter(recipe=recipe)

    steps_list = []
    for line in recipe.steps.split('\n'):
        if line.startswith('Bước'):
            steps_list.append(f"<strong>{line}</strong>")
        else:
            steps_list.append(line)

    parsed_ingredients = []
    seen = set()
    for line in recipe.ingredients.split('\n'):
        line = line.strip()
        if not line or line in seen:
            continue
        seen.add(line)
        if line[0].isdigit():
            parsed_ingredients.append({'type': 'item', 'content': line})
        elif line[0].isalpha() and line[0].isupper():
            parsed_ingredients.append({'type': 'header', 'content': line})
        else:
            parsed_ingredients.append({'type': 'item', 'content': line})

    return render(request, 'dopamine/recipe_detail.html', {
        'recipe': recipe,
        'steps_list': steps_list,
        'detailed_steps': detailed_steps,
        'parsed_ingredients': parsed_ingredients
    })

def all_recipes(request):
    recipe_type = request.GET.get('type', '')
    recipes = Recipe.objects.filter(type=recipe_type) if recipe_type else Recipe.objects.all()
    return render(request, 'dopamine/all_recipes.html', {'recipes': recipes})

def momo_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if request.method == 'POST':
        # Đánh dấu đơn hàng đã hoàn tất
        order.complete = True
        order.save()
        return redirect('thankyou')

    return render(request, 'dopamine/momo_payment.html', {'order': order})