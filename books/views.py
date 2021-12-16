import json

from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Avg

from .models              import Book, Review


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
                "authors"    : [author.author.name for author in book.authorbook_set.all()],
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

class ReViewView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            Review.objects.create(
                user    = request.user.id,
                book_id = data['book_id'],
                rating  = data['rating'],
                content = data['content']
            )

            return JsonResponse({"message":"SUCCESSS"}, status=200)

        except KeyError:
            JsonResponse({"message" : "KEY_ERROR"}, status=400)

    def delete(self, request, review_id):
        Review.objects.filter(user=request.user, id=review_id).delete()
        return JsonResponse({"message" : "NO CONTENT"}, status=204)
