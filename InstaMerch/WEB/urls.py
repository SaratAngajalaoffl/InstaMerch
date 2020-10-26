from django.urls import path

import WEB.views as views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('purchase/', views.purchase_view, name="purchase")
]
