from os import name
from django.urls import path, include

import WEB.views as views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/add-profile-picture/', views.add_profile_pic, name='add_profile_pic'),
    path('post-design/', views.post_design_view,name='post-design'),
    path('design/<str:designid>', views.design_view, name='design_detail'),
    path('cart/',views.show_cart_view,name='cart'),
    path('add-to-cart/<str:designid>',views.add_to_cart_view,name="add-to-cart"),
    path('remove-from-cart/<str:designid>',views.remove_from_cart_view,name="remove-from-cart"),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('orders/',views.orders_view,name='orders'),
    path('manage-addresses/',views.manage_addresses_view,name='manage-addresses'),
    path('my-designs/',views.designs_view,name='my-designs'),
    path('delete-design/<str:designid>',views.delete_design_view,name='delete-design'),
    path('accounts/settings',views.settings_view,name='settings'),
    path('add-address/',views.add_address_view,name='add-address'),
    path('purchase/<str:designid>',views.purchase_view,name='purchase'),
    path('cart-checkout/<str:addressid>',views.cart_checkout_view,name='cart-checkout'),
    path('designs/<str:username>',views.user_designs_view,name='user-designs'),
    path('category/<str:categoryid>',views.designs_by_category_view,name='designs-of-category'),
    path('delete-account/',views.delete_account_view,name='delete_account'),
    path('update-password/',views.update_password_view,name='update_password'),
    path('search/',views.search_view,name='search'),
    path('signGuser/',views.gsignup_view,name='Gsignup'),
    path('', include('social_django.urls', namespace='social')),
    path('done/',views.done_view,name="done"),
]
