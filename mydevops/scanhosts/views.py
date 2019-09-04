import json
import logging

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from scanhosts.models import UserIPInfo, BrowseInfo

logger = logging.getLogger('django')


def user_info(request):
    print(request)
    ip_addr = request.META['REMOTE_ADDR']
    user_ua = request.META['HTTP_USER_AGENT']

    user_obj = UserIPInfo.objects.filter(ip=ip_addr)
    if not user_obj:
        res = UserIPInfo.objects.create(ip=ip_addr)
        ip_addr_id = res.id
    else:
        # logger.info('%s already exists!' % (ip_addr,))
        ip_addr_id = user_obj[0].id
    BrowseInfo.objects.create(useragent=user_ua, userip_id=ip_addr_id)

    result = {
        'STATUS': 'success',
        'INFO': 'User info',
        'IP': ip_addr,
        'UA': user_ua
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def user_history(request):
    ip_list = UserIPInfo.objects.all()
    infos = {}
    for item in ip_list:
        infos[item.ip] = [b_obj.useragent for b_obj in BrowseInfo.objects.filter(userip_id=item.id)]

    result = {
        'STATUS': 'success',
        'INFO': infos
    }
    return HttpResponse(json.dumps(result), content_type='application/json')
