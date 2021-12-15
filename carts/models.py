from django.db import models

from users.models import User
from books.models import Book
from core.utils   import Timer


class Cart(Timer):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    book          = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = "carts"