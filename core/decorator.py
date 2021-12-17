import jwt, os

from django.http  import JsonResponse

from users.models import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get("Authorization",None)
            if token == None:
                request.user = token

                return func(self, request, *args, **kwargs)

            payload      = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=os.environ["ALGORITHM"])
            request.user = User.objects.get(id = payload["id"])

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 404 )
        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status = 400 )
            
    return wrapper