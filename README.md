# Django-JWT
JWT单点登录项目ｄｅｍｏ地址：https://github.com/ly4546/Django-JWT.git
此单点登录是依托于ＤＲＦ接口。
首先在setting文件中修改配置：
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'common.pagination.StandardPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',（主要是修改了用户认证方法，改为ｊｗｔ认证方式）
    )
}
AUTHENTICATION_BACKENDS = (
    'user.views.CustomBackend',（我们自己写的用户认证类，继承django.contrib.auth.backends 的　ModelBackend这个类）
)
ＪＷＴ自己的配置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),（有效时间）
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_ALGORITHM': 'RS256',（非对称加密方式，也有对加密ac256）
　　'JWT_PRIVATE_KEY':'',（私钥）
　　'JWT_PUBLIC_KEY':''，（公钥）
}
然后修改ＵＲＬ的配置：
from rest_framework_jwt.views import obtain_jwt_token（这个接口是rest-jwt自带的接口，实际项目中需要结合实际登录逻辑修改接口）
from user.views import Agent
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', obtain_jwt_token),
    url(r'^api/test/$', Agent.as_view(), name='test'),

]


小结，ＪＷＴ分为ｈｅａｄｅｒ，ｐａｙｌｏａｄ，ｓｉｎｇｎａｔｕｒｅ，在ｄｒｆ-ｊｗｔ中主要应用以下几个方法，在实际项目中，我们可以修改自己的方法。
payload = jwt_payload_handler(user)
token = jwt_encode_handler(payload)
info = jwt_decode_handle(token)

如果不使用DRF接口的形式，只需要下载安装pyjwt包就可以，然后在中间件里面做逻辑判断即可。
class JwtMiddleware(MiddlewareMixin):(中间件形式，放到setting中的MIDDLEWARE中）

    def process_request(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'jwt':
            setattr(request, "user", None)
            return

        if len(auth) == 1 or len(auth) > 2:
            setattr(request, "user", None)
            return

        try:
            jwt_token = auth[1].decode()
            payload = jwt.decode(jwt=jwt_token, key=settings.SECRET_KEY, algorithms=["HS256"])（主要就是运用了ｊｗｔ的decode()方法）
        except Exception as e:
            return HttpResponse('error token, try again !.')

        # 如果token有效期已过
        exp = payload.get('exp')
        user_id = payload.get("u_id")
        if not (exp or user_id) or exp < int(datetime.now().timestamp()):
            setattr(request, 'user', None)
            return

        key = "request_user_{}".format(user_id)
        user = cache.get(key)
        if not user:
            UserModel = get_user_model()
            user = UserModel.objects.get(pk=user_id)
            cache.set(key, user, 3600*2)
        if user.is_active:
            setattr(request, "user", user)
        else:
            setattr(request, "user", None)


