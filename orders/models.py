from django.db import models

from books.models import Book
from users.models import User

from core.utils   import Timer

class Order(Timer):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number   = models.CharField(max_length=500)

    class Meta:
        db_table  = "orders"

class OrderItem(Timer):
    order          = models.ForeignKey("Order", on_delete=models.CASCADE)
    book           = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table  = "order_items"