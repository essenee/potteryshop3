# home/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PotteryCategoryViewSet, ProductByCategoryList

router = DefaultRouter()
router.register(r'pottery-categories', PotteryCategoryViewSet, basename='pottery-category')

urlpatterns = [
    path('api/v2/', include(router.urls)),
    path('api/v2/pottery-items/', ProductByCategoryList.as_view(), name='pottery-items'),
]