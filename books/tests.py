from datetime       import datetime
from django.test    import TestCase, Client

from books.models   import AuthorBook, Book, Author, Review
from users.models   import User
from orders.models  import Order, OrderItem

class BookViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        self.client = Client()
        self.now = datetime.now()
        Book.objects.bulk_create(
            [
                Book(
                    id           = i,
                    name         = f"책{i}",
                    price        = 10000*i,
                    preview_file = "url",
                    file         = "url",
                    description  = f"설명{i}",
                    thumbnail    = f"thumbnail{i}"
                )
                for i in range(1, 4)
            ]
        )

        User.objects.bulk_create(
            [
                User(
                    id          =i,
                    kakao_id    =f"{i}",
                    nickname    =f"닉{i}",
                    profile_img = f"img{i}")
                    for i in range(1, 4)
                ]
            )

        Author.objects.bulk_create([
            Author(
                id   = i,
                name = f"작가{i}"
            ) for i in range(1, 4)
        ])

        AuthorBook.objects.bulk_create(
            [
                AuthorBook(
                    id     = 1,
                    author = Author.objects.get(id=1),
                    book   = Book.objects.get(id=1)), 
                AuthorBook(
                    id     = 2,
                    author = Author.objects.get(id=1),
                    book   = Book.objects.get(id=2)), 
                AuthorBook(
                    id     = 3,
                    author = Author.objects.get(id=2),
                    book   = Book.objects.get(id=2))
                    ]
                )
        
        Review.objects.create(
                user_id  = 1,
                book_id  = 1,
                nickname = "Q",
                rating   = 5,
                content  = "123"
        )

        Order.objects.create(
            id           = 1,
            user         = User.objects.get(id=1),
            order_number = "1234"
        )

        OrderItem.objects.create(
            id    = 1,
            order = Order.objects.get(id=1),
            book  = Book.objects.get(id=1)
        )

    def tearDown(self):
        Book.objects.all().delete()
        Author.objects.all().delete()
        AuthorBook.objects.all().delete()
        User.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()

    
    def test_success_book_view_review_list_view_get_method(self):
        response = self.client.get('/books/1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            "result": 
                {
                    "purchased"  : False,
                    "name"       : "책1",
                    "price"      : "10000.00",
                    "description": "설명1",
                    "thumbnail"  : "thumbnail1",
                    'average':   {'avg_rating': '5.000000'},
                    "authors"    : [
                        "작가1"
                    ],
                }
            
        })