from django.utils import timezone
from django.test import TestCase, Client
TestCase.maxDiff = None

from books.models import AuthorBook, Book, Author, Review
from users.models import User

class JustTest(TestCase):
    maxDiff = None
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()
        Book.objects.bulk_create(
            [
                Book(
                    id=i,
                    name=f"책{i}",
                    price=10000*i,
                    preview_file="url",
                    file="url",
                    description=f"설명{i}",
                    thumbnail=f"thumbnail{i}"
                )
                for i in range(1, 4)
            ]
        )

        User.objects.bulk_create(
            [
                User(
                    id=i,
                    kakao_id=f"{i}",
                    nickname=f"닉{i}",
                    profile_img = f"img{i}")
                    for i in range(1, 4)
                ]
            )

        Author.objects.bulk_create([
            Author(
                id=i,
                name=f"작가{i}"
            ) for i in range(1, 4)
        ])

        AuthorBook.objects.bulk_create(
            [
                AuthorBook(
                    id=1,
                    author=Author.objects.get(id=1),
                    book=Book.objects.get(id=1)), 
                AuthorBook(
                    id=2,
                    author=Author.objects.get(id=1),
                    book=Book.objects.get(id=2)), 
                AuthorBook(
                    id=3,
                    author=Author.objects.get(id=2),
                    book=Book.objects.get(id=2))
                    ]
                )

        Review.objects.bulk_create(
            [
                Review(
                    id=1,
                    user=User.objects.get(id=1), 
                    book=Book.objects.get(id=1),
                    rating=5,content="content1", 
                    created_at = "2021-12-16"),
                Review(
                    id=2,
                    user=User.objects.get(id=1), 
                    book=Book.objects.get(id=1),
                    rating=6,
                    content="content2",
                    created_at = "2021-12-16"), 
                Review(
                    id=3,
                    user=User.objects.get(id=2), 
                    book=Book.objects.get(id=1),
                    rating=7,
                    content="content3",
                    created_at = "2021-12-16")
                    ]
                )
    

    def test_success_book_view_review_list_view_get_method(self):
        response = self.client.get('/books/1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            "result": [
                {
                    "name"       : "책1",
                    "price"      : "10000.00",
                    "discription": "설명1",
                    "thumbnail"  : "thumbnail1",
                    "authors"    : [
                        "작가1"
                    ],
                    "average"    : {
                        "rating__avg": "6.000000"
                    },
                    "reviews"    : [
                        {
                            "user"      : "닉1",
                            "rating"    : "5.00",
                            "content"   : "content1",
                            "created_at": self.now
                        },
                        {
                            "user"      : "닉1",
                            "rating"    : "6.00",
                            "content"   : "content2",
                            "created_at": self.now
                        },
                        {
                            "user"      : "닉2",
                            "rating"    : "7.00",
                            "content"   : "content3",
                            "created_at": self.now
                        }
                    ]
                }
            ]
        })