from django.contrib import admin
from products import views
from django.urls import include, path
from register.views import register_request, login_request, logout_request, update_profile, profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'), #home page url
    path('products/', include('products.urls')), #products/index page url
    path('register/', register_request, name="register"), #register page url
    path('login/', login_request, name="login"),  #login page url
    path('logout/', logout_request, name="logout"), #logout url
    path('update/', update_profile, name="update_profile"), #profile update url
    path('admin/', admin.site.urls), #admin site url
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)