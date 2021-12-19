from django.views import View
from django.http  import JsonResponse

from orders.models  import OrderItem
from core.decorator import login_required

class OrderItemView(View):
    @login_required
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

        id__in = [1,2,3,4,5]
        cart.delete()