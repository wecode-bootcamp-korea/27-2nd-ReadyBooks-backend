from django.urls import path

from .views import OrderItemView, OrderView

urlpatterns = [
    path("/orderitems",OrderItemView.as_view()),
    path("",OrderView.as_view())
]