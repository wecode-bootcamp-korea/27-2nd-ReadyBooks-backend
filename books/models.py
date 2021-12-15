from django.db    import models

from core.utils   import Timer
from users.models import User

class Book(Timer):
    name          = models.CharField(max_length=200)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    preview_file  = models.URLField(max_length=1000)
    file          = models.URLField(max_length=1000)
    description   = models.TextField(max_length=2000)
    thumbnail     = models.URLField(max_length=1000)

    class Meta:
        db_table = "books"
    
    def __str__(self):
        return self.name

class Reply(Timer):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    book          = models.ForeignKey("Book", on_delete=models.CASCADE)
    book_page     = models.IntegerField()
    content       = models.TextField(max_length=1000)

    class Meta:
        db_table = "replies"

    def __str__(self):
        return self.content

class AuthorBook(models.Model):
    author          = models.ForeignKey("Author", on_delete=models.CASCADE)
    book            = models.ForeignKey("Book", on_delete=models.CASCADE)

    class Meta:
        db_table   = "author_books"
        constraints = (models.UniqueConstraint(fields=["author", "book"], name='unique author and book'),)

class Author(models.Model):
    name            = models.CharField(max_length=200)

    class Meta:
        db_table   = "authors"

    def __str__(self):
        return self.name

class Review(Timer):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    book          = models.ForeignKey("Book", on_delete=models.CASCADE)
    rating        = models.DecimalField(max_digits=10, decimal_places=2)
    content       = models.TextField(max_length=1000)

    class Meta:
        db_table = "reviews"
    
    def __str__(self):
        return self.content

