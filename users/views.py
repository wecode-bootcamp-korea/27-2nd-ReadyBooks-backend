import jwt, os

from django.http  import JsonResponse
from django.views import View

from .models      import User
from core.kakao   import KakaoApi

class SignInView(View):
    def get(self, request):
        try:
            kakao_user      = KakaoApi(request.headers["Authorization"])
            kakao_user_data = kakao_user.get_kakao_user()

            user, created = User.objects.get_or_create(
                kakao_id = kakao_user_data["id"], 
                defaults = {
                    "nickname"    : kakao_user_data["kakao_account"]["profile"]["nickname"],
                    "profile_img" : kakao_user_data["kakao_account"]["profile"]["profile_image_url"]
                }
            )
            token = jwt.encode({"id" : user.id}, os.environ["SECRET_KEY"], algorithm = os.environ["ALGORITHM"])
            
            return JsonResponse({
                "Authorization"    : token,
                "user_nickname"    : user.nickname, 
                "user_profile_img" : user.profile_img,
                "user_id"          : user.id }, status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        except User.MultipleObjectsReturned:
            return JsonResponse({"message" : "MULTIPLE_OBJECT_RETURNED"}, status = 400)