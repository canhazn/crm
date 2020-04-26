from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer/<int:id>', views.customer, name='customer'),
    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<int:id>', views.updateOrder, name='update_order'),
    path('delete_order/<int:id>', views.deleteOrder, name='delete_order'),
]