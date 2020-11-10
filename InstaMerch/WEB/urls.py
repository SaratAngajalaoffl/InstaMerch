from django.urls import path, include

import WEB.views as views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('purchase/', views.purchase_view, name="purchase"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register_view, name='register'),
    path('designs/<str:designid>', views.design_view, name='design_detail')
]
