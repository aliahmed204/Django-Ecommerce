from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='store.cart'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('checkout/', views.checkout, name='store.checkout'),
    path('processOrder/', views.processOrder, name='store.processOrder'),
]
