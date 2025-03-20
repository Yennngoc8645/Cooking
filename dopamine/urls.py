from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name= "home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('admin/', admin.site.urls),
    path('update_item/', views.updateItem, name="update_item"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

