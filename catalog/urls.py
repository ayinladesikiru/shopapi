from django.urls import path, include
from .views import ProductViewSet, get_product_by_category, CartViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('carts', CartViewSet, basename='carts')


urlpatterns = [
    path('', include(router.urls)),
    path('categories/<slug:slug>/', get_product_by_category, name='product_list_by_category'),
]

# urlpatterns += router.urls