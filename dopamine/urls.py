from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name= "home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('recipes/', views.all_recipes, name='all_recipes'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('category/', views.category, name="category"),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('checkout/', views.checkout, name="checkout"),
    path('admin/', admin.site.urls),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.process_order, name='process_order'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('search/', views.search, name='search'),
    path('ajax/autocomplete/', views.autocomplete_products, name='autocomplete_products'),
    path('thanh-toan-momo/<int:order_id>/', views.momo_payment, name='momo_payment'),
    path('momo-payment/<int:order_id>/', views.momo_payment, name='momo_payment'),
    path('thong-ke/', views.thong_ke_hang_ban, name='thong_ke'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

