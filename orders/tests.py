from django.test    import TestCase
from django.test    import Client

from books.models   import Book, Author, AuthorBook
from orders.models  import Order, OrderItem
from users.models   import User

class OrderBookTest(TestCase):
    def setUp(self):
        user = User.objects.create(
        id       = 1,
        nickname = '성종호',
        kakao_id = 1
        )

        Order.objects.create(
            id   = 1,
            user = user
        )

        bulk_book = [
            Book(
                id        = 1,
                name     = '홍길동전',
                thumbnail = "img.jpg",
                price = 1000
        ), 
            Book(
                id        = 2,
                name     = '해리포터',
                thumbnail = "img.jpg",
                price = 1000
        )]
        Book.objects.bulk_create(bulk_book)

        bulk_author = [
            Author(
                id    = 1,
                name  = '강아지',
        ),
            Author(
                id    = 2,
                name  = '고양이',
        )]
        Author.objects.bulk_create(bulk_author)

        bulk_authorbook = [
            AuthorBook(
                book   = Book.objects.get(id=1),
                author = Author.objects.get(id=1)
                ),
            AuthorBook(
                book   = Book.objects.get(id=1),
                author = Author.objects.get(id=2)
                ),
            AuthorBook(
                book   = Book.objects.get(id=2),
                author = Author.objects.get(id=1)
                ),
            AuthorBook(
                book   = Book.objects.get(id=2),
                author = Author.objects.get(id=2)
                )
        ]
        AuthorBook.objects.bulk_create(bulk_authorbook)
     
        bulk_orderitem = [
            OrderItem(
                id       = 1,
                book_id  = 1,    
                order_id = 1
            ),
            OrderItem(
                id       = 2,
                book_id  = 2,    
                order_id = 1
            )
        ]
        OrderItem.objects.bulk_create(bulk_orderitem)
    
    def tearDown(self):
        Book.objects.all().delete()
        Author.objects.all().delete()
        AuthorBook.objects.all().delete()
        User.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete

    def test_order_book_get_success(self):
        client   = Client()
        response = client.get('/orders/orderitems')
        print(response.json())
        self.assertEqual(response.json(),{"result":[
            {
            "order_id"   : 2,
            "order_book" : {
                "id"          : 2,
                "title"        : "해리포터",
                "thumbnail"   : "img.jpg",
                "author" : ["강아지","고양이"]
                }
            },{
            "order_id"   : 1,
            "order_book" : {
                "id"          : 1,
                "title"        : "홍길동전",
                "thumbnail"   : "img.jpg",
                "author" : ["강아지","고양이"]
            }}]})
        self.assertEqual(response.status_code, 200)