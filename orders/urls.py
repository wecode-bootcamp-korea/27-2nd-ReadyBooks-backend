from django.urls import path

from .views import OrderItemView

urlpatterns = [
    path("/orderitems",OrderItemView.as_view(),)
]