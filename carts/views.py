import json

from django.http        import JsonResponse
from django.views       import View

from core.decorator import login_required
from books.models import Book
from carts.models import Cart

class CartView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            book_id = data['book_id']
                
            if Cart.objects.filter(user = user, book_id = book_id).exists():
                return JsonResponse({"message" : "BOOK_ALREADY_EXIST"}, status=400)  
                
            Cart.objects.create(user = user, book_id = book_id)
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
    @login_required
    def get(self, request):
        carts = Cart.objects.prefetch_related('book__authorbook_set__author').filter(user=request.user).order_by('-created_at')
        
        result = [{
            'cart_id'   : cart.id,
            'book_id'   : cart.book.id,
            'title'     : cart.book.name,
            'price'     : cart.book.price,
            'thumbnail' : cart.book.thumbnail,
            'author'    : [authors.author.name for authors in cart.book.authorbook_set.all()]
        } for cart in carts ]

        return JsonResponse({"result" : result}, status=200)
    
    @login_required
    def delete(self, request):
        
        Cart.objects.filter(id__in = request.GET.getlist("cart_id"), user = request.user).delete()            
        
        return JsonResponse({"message" : "NO_CONTENTS"}, status=204)