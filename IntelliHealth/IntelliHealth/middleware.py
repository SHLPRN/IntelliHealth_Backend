from utils.token import check_token
from django.http import JsonResponse

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object


API_WHITELIST = ["/api/user/login/", ]


class AuthorizeMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if request.path not in API_WHITELIST:
            token = request.META.get('HTTP_TOKEN')
            if token is None or token == '':
                return JsonResponse({'errno': 1001, 'msg': "未查询到登录信息"})
            else:
                if check_token(token):
                    if request.path == '/api/user/checkToken/':
                        return JsonResponse({'errno': 0, 'msg': '成功'})
                    else:
                        pass
                else:
                    return JsonResponse({'errno': 1002, 'msg': "登录已过期"})
