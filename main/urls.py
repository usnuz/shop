from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', categories),
    path('subcategories/', subcategories),
    path('products/', products),
    path('promo/', promo),
    path('create-product/', create_product),
    path('order/', order),
    path('is-slider/', is_slider),
    path('wishlist/', wishlist),
    path('card/', cards),
]
