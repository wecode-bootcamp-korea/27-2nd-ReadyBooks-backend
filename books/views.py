from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg

from books.models  import Review

class BookRankingView(View):
    def get(self, request):
        
        reviews = Review.objects.all().annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:10]
        
        rank_list=[{
            'title'     : review.book.name,
            'thumbnail' : review.book.thumbnail,
            'rating'    : review.rating
        } for review in reviews]

        return JsonResponse({'result' : rank_list}, status = 200)