from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('category/<slug:slug>/', ProductListCategory.as_view(), name='category_list'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('login_registration/', login_registration, name='login_registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('save_review/<slug:product_slug>/', save_review, name='save_review'),
    path('add-or-delete-favourite/<slug:product_slug>/', save_or_delete_fav_products, name='save_or_delete'),
    path('favourite-products/', FavouriteProductsView.as_view(), name='favourite_products'),
    path('card/', cart, name='card'),
    path('to_card/<int:product_id>/<str:action>/', to_card, name='to_card'),
    path('checkout/', checkout, name='checkout')

]
