import jwt,json

from datetime            import datetime
from django.test         import TestCase
from django.test         import Client

from readybooks.settings import SECRET_KEY,ALGORITHM
from users.models        import User
from books.models        import Book, Author, AuthorBook
from users.models        import User
from carts.models        import Cart

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.now = datetime.now()
        

        user = User.objects.create(

        nickname     = '성주호',
        kakao_id     = 55,
        profile_img  = 'url'
        )

        bulk_book = [
            Book(
                id        = 1,
                name      = '홍길동전',
                thumbnail = "image",
                price = 1000
        ), 
            Book(
                id        = 2,
                name      = '해리포터',
                thumbnail = "image",
                price = 1000
        ),
            Book(
                id        = 3,
                name      = '인어공주',
                thumbnail = "image",
                price = 1000
        ),]
        Book.objects.bulk_create(bulk_book)
        
        bulk_cart = [
            Cart(
            id   = 1,
            book = bulk_book[0],
            user = user
        ),
            Cart(
            id   = 2,
            book = bulk_book[1],
            user = user
        )]
        Cart.objects.bulk_create(bulk_cart)

        bulk_author = [
            Author(
                id    = 1,
                name  = '영작가',
        ),
            Author(
                id    = 2,
                name  = '한작가',
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
        
        self.token = jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        Book.objects.all().delete()
        Author.objects.all().delete()
        AuthorBook.objects.all().delete()
        User.objects.all().delete()
        Cart.objects.all().delete()


    def test_cart_get_success(self):
        client = Client()
        headers = {"HTTP_Authorization" : self.token}
        
        response = client.get('/carts',**headers)

        self.assertEqual(response.json(),{
            "result":[
            {
                "cart_id"   : 2,
                "book_id"   : 2,
                "title"     : "해리포터",
                'price'     : "1000.00",
                "thumbnail" : "image",
                "author"    : ["영작가","한작가"]
                },
            {
                "cart_id"   : 1,
                "book_id"   : 1,
                "title"     : "홍길동전",
                'price'     : "1000.00",
                "thumbnail" : "image",
                "author"    : ["영작가","한작가"]
                }
            ]
        })
        self.assertEqual(response.status_code, 200) 

    def test_cart_post_success(self):
        client = Client()
        
        headers = {"HTTP_Authorization" : self.token}
        
        book_id = {'book_id' : 3}

        response = client.post('/carts', json.dumps(book_id), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {
            'message': "SUCCESS"
        })
        self.assertEqual(response.status_code, 201)
        
    def test_cart_delete_success(self):
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.delete('/carts?1&2', **headers)
        
        self.assertEqual(response.status_code, 204)