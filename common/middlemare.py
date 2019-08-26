import re
import jwt
import datetime
from django.utils.deprecation import MiddlewareMixin

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_jwt.utils import jwt_decode_handler


def user_auth_handler(get_response):
    ''' user auth info handler '''

    def middleware(request):

        try:
            auth = request.META.get('HTTP_AUTHORIZATION')
            if not auth:
                auth = request.POST.get('_authorization')
            # auth = re.match(r'bearer\s(\w+\.\w+\..+)', auth)
            auth = jwt_decode_handler(auth)
            exp = auth.get('exp', 0)
            if exp < datetime.datetime.now().timestamp():
                setattr(request, 'user', None)
            else:
                user_id = auth.get('user_id')
                UserModel = get_user_model()
                user = UserModel.objects.get(pk=user_id)
                if user.is_active:
                    print(user.is_active)
                    setattr(request, 'user', user)
                else:
                    print(user.is_active)
                    setattr(request, 'user', None)
        except:
            setattr(request, 'user', None)

        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    return middleware

class NotifySalesTokenMiddleware(MiddlewareMixin):
    """判断销售代表是否合法"""

    def process_request(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            auth = request.POST.get('_authorization')
        print(auth)

        # auth = jwt_decode_handler(auth)
        # print(auth)
        # user_id = auth.get('user_id')
        # UserModel = get_user_model()
        # user = UserModel.objects.get(pk=user_id)
        # if user.is_active:
        #     print(user.is_active)
        #     print('sdfsdfsdf')
        #     print(user)
        #     setattr(request, 'user', user)
        # else:
        #     print(user.is_active)
        #     print(123333)
        #     setattr(request, 'user', None)


def jwt_get_username_from_payload_handlers(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get('mobile')
