from django.urls import path, include

import WEB.views as views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('purchase/', views.purchase_view, name="purchase"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/add-profile-picture/', views.add_profile_pic, name='add_profile_pic'),
    path('designs/<str:designid>', views.design_view, name='design_detail'),
    path('designs/post-design', views.post_design_view,name='post-design')
]
