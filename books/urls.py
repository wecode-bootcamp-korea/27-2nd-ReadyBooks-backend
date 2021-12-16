from django.urls import path

from .views import BookView

urlpatterns = [
    path("/<int:book_id>",BookView.as_view())
]