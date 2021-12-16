import json
from django.views           import View

from django.http.response   import JsonResponse
from django.db.models.query import Prefetch
from django.db.models       import Avg 

from .models                import Book, Review
from orders.models          import OrderItem
from core.decorator         import login_required, public_authorization

class BookView(View):
    @public_authorization
    def get(self, request, book_id):
        try:
            book    = Book.objects.prefetch_related('authorbook_set__author', "review_set",Prefetch("orderitem_set", OrderItem.objects.filter(order__user=request.user))).get(id=book_id)

            results={
                "purchased"    : bool(book.orderitem_set.all()),
                "name"         : book.name,
                "price"        : book.price,
                "description"  : book.description,
                "preview_file" : book.preview_file,
                "file"         : book.file,
                "thumbnail"    : book.thumbnail,
                "average"      : book.review_set.aggregate(avg_rating=Avg('rating')),
                "authors"      : [author.author.name for author in book.authorbook_set.all()]
            }

            return JsonResponse({"result":results}, status=200)

        except Book.DoesNotExist:
            JsonResponse({"message" : "DOES_NOT_EXIST"}, status=401)


class BooksView(View):
    @login_required
    def get(self, request):
        limit    = int(request.GET.get('limit', 50))
        offset   = int(request.GET.get('offset', 0))
        ordering = request.GET.get('ordering', 'created_at')

        books = Book.objects.annotate(review_avg = Avg('review__rating')).prefetch_related('authorbook_set__author').order_by(ordering)[offset:limit+offset]

        book_list=[{
            "title"      : book.name,
            "thumbnail"  : book.thumbnail,
            "review_avg" : book.review_avg,
            "authors"    : [author.author.name for author in book.authorbook_set.all()]
        } for book in books]

        return JsonResponse({'result' : book_list}, status = 200)

class ReviewView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)

            Review.objects.create(
                user     = request.user,
                book_id  = data['book_id'],
                nickname = data['nickname'],
                rating   = data['rating'],
                content  = data['content']
            )
            return JsonResponse({"message":"SUCCESSS"}, status=200)

        except KeyError:
            JsonResponse({"message" : "KEY_ERROR"}, status=400)

    def get(self, request):
        book = request.GET.get("book_id", None)
        results = []
        
        results.append({
            "book_id"        : book,
            "average"        : Review.objects.filter(book_id=book).aggregate(avg_rating=Avg('rating')),
            "review"         :
            [{
                "review_id"  : review.id,
                "user_id"    : review.user_id,
                "nickname"   : review.nickname,
                "rating"     : review.rating,
                "content"    : review.content,
                "created_at" : review.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for review in Review.objects.filter(book_id= book)]
        })
        return JsonResponse({"result" : results}, status=200)

    @login_required
    def delete(self, request, review_id):
        Review.objects.filter(user=request.user, id=review_id).delete()
        return JsonResponse({"message" : "NO CONTENT"}, status=204)
