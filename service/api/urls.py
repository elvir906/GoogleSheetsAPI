from django.urls import path

from api import views

urlpatterns = [
  path('orders/', views.get_chunk),
]
