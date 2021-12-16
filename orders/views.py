import json, uuid

from django.views   import View
from django.http    import JsonResponse

from django.db      import transaction

from orders.models  import OrderItem, Order
from carts.models   import Cart
from core.decorator import login_required, public_authorization

class OrderItemView(View):
    @public_authorization
    def get(self, request):
        items = OrderItem.objects.filter(order__user=request.user).prefetch_related("book__authorbook_set__author").order_by("-created_at")[0:10]
        result = [{
            "order_id"   : item.id,
            "order_book" : { 
                "id"        : item.book.id,
                "title"     : item.book.name,
                "thumbnail" : item.book.thumbnail,
                "author"    : [authors.author.name for authors in item.book.authorbook_set.all()]}
        } for item in items]

        return JsonResponse({"result":result}, status=200 )

class OrderView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        books = data['cart_id']
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user = user,
                    order_number = uuid.uuid4()
                )
                order_items = [OrderItem(
                    order   = order,
                    book_id = book
                )for book in books]
            
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(book_id__in=books).delete()

            return JsonResponse({'message':order.order_number}, status=201)
        
        except transaction.TransactionManagementError:
            return JsonResponse({'message':'TransactionManagementError'}, status=401)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)
