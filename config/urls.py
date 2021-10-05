"""GIZ_YANHAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from config.utils.permissions import AuthBearer
from account.views import auth_controller
from commerce import views

api = NinjaAPI(
    version='1.0.0',
    title='Commerce API v1',
    description='API documentation',
    auth=AuthBearer()
)

api.add_router('auth', auth_controller)
api.add_router('address', views.address)
api.add_router('vendor', views.vendor)
api.add_router('product', views.product)
api.add_router('order', views.order)
api.add_router('item', views.item)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
