from django.db import models

from utils     import Timer


class User(Timer):
    kakao_id    = models.IntegerField()
    nickname    = models.CharField(max_length=500)
    profile_img = models.URLField(max_length=1000)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.nickname