from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name= "home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('admin/', admin.site.urls),
=======
    path('', views.home),
    path('admin/', admin.site.urls),  # Bao gồm URL admin
>>>>>>> 7f16a977cc46fa46b912e2039ef97e6a39e11695
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

