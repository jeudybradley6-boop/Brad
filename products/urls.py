from django.urls import path
from . import views

urlpatterns = [
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
     
    path('commande/success/', views.commande_success, name='commande_success'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]