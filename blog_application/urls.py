"""
URL configuration for blog_application project.

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
from django.urls import path,include
# from home.views import home_page
from django.conf import settings
from django.conf.urls.static import static
from login.views import register_user,user_login,user_logout
from post.views import postCategory

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',home_page,name='home'), 
    
    path('api_login/',include('login.urls')),
    path('api_post/',include('post.urls')),
    path('api_images/',include('Images.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)