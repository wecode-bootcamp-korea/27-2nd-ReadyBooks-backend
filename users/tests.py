import jwt, os

from django.test   import Client, TestCase
from unittest.mock import patch, MagicMock

class SignInTest(TestCase):
    @patch("core.kakao.requests")
    def test_kakao_signin_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):

                return {
                    "id":114142,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "성종호",
                            "thumbnail_image_url": "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url": "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image":False
                            }
                        }
                    }
                    
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "가짜 access_token"}
        response            = client.get("/users/kakao/signin", **headers)
        token               = jwt.encode({"id" : 1}, os.environ["SECRET_KEY"], os.environ["ALGORITHM"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Authorization': token,
            'user_id': 1,
            'user_nickname': '성종호',
            'user_profile_img': 'http://yyy.kakao.com/dn/.../img_640x640.jpg'
        })

    @patch("core.kakao.requests")
    def test_kakao_signin_client_get_key_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):

                return {
                    "id":114142,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "성종호",
                            "thumbnail_image_url": "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url": "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image":False
                            }
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorizatio" : "가짜 access_token"} 
        response            = client.get("/users/kakao/signin", **headers)
   
        self.assertEqual(response.json(), {'message' : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)