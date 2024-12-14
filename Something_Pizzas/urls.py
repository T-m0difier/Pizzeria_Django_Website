"""
URL configuration for Epic_Pizzas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('profile/', profile, name="profile"),  # Profile page URL  
    path('profile/update/', update_profile, name="update_profile"), #profile update url
    path('admin/', admin.site.urls), #admin site url
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)