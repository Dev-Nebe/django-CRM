from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<int:customer_id>', views.customer, name="customer"),
    path('orders/<int:customer_id>', views.createOrder, name="create_order"),
    path('orders/<int:order_id>', views.updateOrder, name='update_order'),
    path('orders/<int:order_id>/delete', views.deleteOrder, name="delete_order")
]
