from django.urls import path

from .views import BookView,BooksView, ReviewView

urlpatterns = [
    path("/<int:book_id>",BookView.as_view()),
    path('/main', BooksView.as_view()),
    path('/review', ReviewView.as_view()),
    path("/review/<int:review_id>",ReviewView.as_view())
]

