from django.db import models

from books.models import Book
from users.models import User


class Order(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number   = models.CharField(max_length=500)
    created_at     = models.DateTimeField(auto_now_add=False)
    updated_at     = models.DateTimeField(auto_now=False)

    class Meta:
        db_table  = "orders"

class OrderItem(models.Model):
    order          = models.ForeignKey("Order", on_delete=models.CASCADE)
    book           = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table  = "order_items"