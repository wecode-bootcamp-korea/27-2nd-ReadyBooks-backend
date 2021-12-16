import json, jwt

from datetime       import datetime
from django.utils import timezone
from django.test    import TestCase, Client

from books.models   import AuthorBook, Book, Author, Review
from users.models   import User
from orders.models  import Order, OrderItem

from readybooks.settings import SECRET_KEY, ALGORITHM

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
                    "purchased"    : False,
                    "name"         : "책1",
                    "price"        : "10000.00",
                    "description"  : "설명1",
                    "preview_file" : "url",
                    "file"         : "url",
                    "thumbnail"    : "thumbnail1",
                    'average'      :   {'avg_rating': '5.000000'},
                    "authors"      : [
                        "작가1"
                    ],
                }
        })

class BooksViewTest(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.client = Client()
        
        User.objects.create(
            id          = 1,
            kakao_id    = '11',
            nickname    = '현대영작가',
            profile_img = 'image'
        )
        
        Book.objects.create(id = 2,name = '해리포터',price = 12300,preview_file = 'image', \
                                 file = 'images',description = '20주년',thumbnail = 'images')
        
        Author.objects.create(id = 1,name = '현대영작가')
        
        AuthorBook.objects.create(id = 1,author = Author.objects.get(id=1),book = Book.objects.get(id=2))
        
        Review.objects.create(user_id  = 1,book_id  = 2,rating = 4.6)
        

          
    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        AuthorBook.objects.all().delete()
        Review.objects.all().delete()

    def test_success_get_books(self):
        response = self.client.get('/books/main')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(), {
            "result" : [
                {
                    "title"      : "해리포터",
                    "thumbnail"  : "images",
                    "review_avg" : 1.0,
                    "authors"    : ["현대영작가"]
                }
            ]
        })


    
    def test_success_get_books_offset_and_limit(self):
        response = self.client.get('/books/main?limit=12&offset=0')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(), {
            "result" : [
                {
                    "title"      : "해리포터",
                    "thumbnail"  : "images",
                    "review_avg" : 2.0,
                    "authors"    : ["현대영작가"]
                }
            ]
        })

class ReViewPostTest(TestCase):
    maxDiff = None
    
    def setUp(self):
        self.client = Client()

        Book.objects.create(
            id=1,
            name="책1",
            price=10000,
            preview_file="url",
            file="url",
            description="설명1",
            thumbnail="thumbnail1"
        )

        User.objects.create(
            id=1,
            kakao_id=1,
            nickname="닉1",
            profile_img = "img1"
        )

        self.token = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        

    def tearDown(self):
        Book.objects.all().delete()
        User.objects.all().delete() 
    

    def test_success_review_view_post_method(self):
        client = Client()

        headers = {"HTTP_Authorization" : self.token}

        review = {
            "nickname" : 'Q',
            "rating"   : 4,
            "content"  : '123'
        }

        response = client.post('/books/review/1', json.dumps(review), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {
            'message': 'SUCCESSS'
        })

        self.assertEqual(response.status_code, 200)


