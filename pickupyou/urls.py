"""pickupyou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import routers

from pickupyou.schedule import views
from pickupyou.schedule.views import (
    OrderDetail, DriverOrdersDetail, NearestDriverDetail
)


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Schedule API",
        default_version='1.0.0',
        description="API documentation of Pick-up You",
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'coordinates', views.CoordinatesViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    re_path('^orders/(?P<day>.+)/$', OrderDetail.as_view()),
    re_path(
        '^drivers/(?P<pk>.+)/orders/(?P<day>.+)/$',
        DriverOrdersDetail.as_view()
    ),
    re_path('^nearest-driver/', NearestDriverDetail.as_view()),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name="schema-swagger-ui"),
]
