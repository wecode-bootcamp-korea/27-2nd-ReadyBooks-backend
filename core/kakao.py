import requests

from django.views import View
from django.http  import JsonResponse

class KakaoApi(View):
        def __init__(self, token):
            self.token     = token
            self.kakao_url = "https://kapi.kakao.com/v2/user/me"
            self.headers   = {"Authorization":"Bearer " + self.token}

        def get_kakao_user(self):
            try:
                kakao_data = requests.get(self.kakao_url, headers = self.headers, timeout=3).json()

                return kakao_data

            except requests.Timeout:
                return JsonResponse({"message" : "REQUESTS_TIMEOUT"}, status = 400)