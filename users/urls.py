from django.urls import path

from .views import SignInView

urlpatterns = [
    path("/kakao/signin",SignInView.as_view(),)
]