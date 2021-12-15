from django.views         import View

from django.http.response import JsonResponse

from django.db.models import Avg

from .models              import Book
from readybooks.settings  import ACCESS_KEY, ACCESS_SECRET_KEY


class BookView(View):
    def get(self, request, book_id):
        try:
            book    = Book.objects.prefetch_related('authorbook_set__author','review_set').get(id=book_id)
            results = []

            results.append({
                "name"       : book.name,
                "price"      : book.price,
                "discription": book.description,
                "thumbnail"  : book.thumbnail,
                "authors"     : [author.author.name for author in book.authorbook_set.all()],
                "average"    : book.review_set.all().aggregate(Avg('rating')),
                "reviews"    : 
                [{  "user"       : review.user.nickname,
                    "rating"     : review.rating,
                    "content"    : review.content,
                    "created_at" : review.created_at
                }for review in book.review_set.all()]
            })
            return JsonResponse({"result":results}, status=200)

        except Book.DoesNotExist:
            JsonResponse({"message" : "DOES_NOT_EXIST"}, status=401)