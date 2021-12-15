import os
import django
import csv
import sys
  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "readybooks.settings")
django.setup()

from users.models import User
from books.models import AuthorBook, Book, Author, Review


# CSV_PATH = '/Users/jinsungpark/Downloads/user.csv'

# with open(CSV_PATH, newline='') as csvfile:
#     data_reader = csv.DictReader(csvfile)
#     for row in data_reader:
#         print(row)
#         User.objects.create(
#             kakao_id = row['kakao_id'],
#             nickname = row['nickname'],
#             profile_img = row['profile_img']
#         )

# CSV_PATH = '/Users/jinsungpark/Downloads/author.csv'

# with open(CSV_PATH, newline='') as csvfile:
#     data_reader = csv.DictReader(csvfile)
#     for row in data_reader:
#         print(row)
#         Book.objects.create(
#             name = row['name'],
#             price = row['price'],
#             preview_file = row['preview_file'],
#             file = row['file'],
#             description = row['description'],
#             thumbnail = row['thumbnail']
#         )

CSV_PATH = '/Users/jinsungpark/Downloads/review.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        print(row)
        Review.objects.create(
            rating = row['rating'],
            content = row['content'],
            book_id = row['book_id'],
            user_id = row['user_id']
        )