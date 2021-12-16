from django.urls import path

from .views import BookView,BooksView

urlpatterns = [
    path("/<int:book_id>",BookView.as_view()),
    path('/main', BooksView.as_view()),
]
