import functools
import json

from django.http import JsonResponse
from django.contrib.sessions.models import Session

from ubskin_site.member_manage import models as member_model

def js_authenticated(fuc):
    @functools.wraps(fuc)
    def wrapper(request, *args, **kwargs):
        return_data = dict()
        if str(request.user) == "AnonymousUser":
            return_data["message"] = "你没有登陆"
            return_data["status"] = "error"
            return JsonResponse(return_data)
        return fuc(request, *args, **kwargs)
    return wrapper

