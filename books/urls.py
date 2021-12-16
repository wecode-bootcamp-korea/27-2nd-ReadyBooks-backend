from django.urls import path

from .views import BookView, ReViewView

urlpatterns = [
    path("/<int:book_id>",BookView.as_view()),
    path("/review", ReViewView.as_view())
]