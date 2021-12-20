from django.views           import View

from django.http.response   import JsonResponse
from django.db.models.query import Prefetch
from django.db.models       import Avg 

from .models                import Book
from orders.models          import OrderItem
from core.decorator         import login_required

class BookView(View):
    @login_required
    def get(self, request, book_id):
        try:
            book    = Book.objects.prefetch_related('authorbook_set__author', "review_set",Prefetch("orderitem_set", OrderItem.objects.filter(order__user=request.user))).get(id=book_id)

            results={
                "purchased"  : bool(book.orderitem_set.all()),
                "name"       : book.name,
                "price"      : book.price,
                "description": book.description,
                "thumbnail"  : book.thumbnail,
                "average"    : book.review_set.aggregate(avg_rating=Avg('rating')),
                "authors"    : [author.author.name for author in book.authorbook_set.all()]
            }

            return JsonResponse({"result":results}, status=200)

        except Book.DoesNotExist:
            JsonResponse({"message" : "DOES_NOT_EXIST"}, status=401)