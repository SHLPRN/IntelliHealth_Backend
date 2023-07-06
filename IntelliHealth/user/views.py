import os
import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *
from utils.token import *
from utils.sms import sms_sender

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')


RECORD_IMAGE_URL = '/media/record/'


@csrf_exempt
def login(request):
    users = User.objects.filter(phone=request.POST.get('phone'))
    if len(users) == 0:
        return JsonResponse({'errno': 1004, 'msg': '用户不存在'})
    user = users.first()
    password = request.POST.get('password')
    if user.password != password:
        return JsonResponse({'errno': 1005, 'msg': '密码错误'})
    token = create_token('user', user.id)
    return JsonResponse({'errno': 0, 'msg': '登录成功', 'token': token})


@csrf_exempt
def get_user_info(request):
    user = User.objects.get(id=int(get_id(request.META.get('HTTP_TOKEN'))))
    return JsonResponse({
        'errno': 0,
        'id': user.id,
        'name': user.name,
        'nickname': user.nickname,
        'phone': user.phone
    })


@csrf_exempt
def add_record(request):
    user = User.objects.get(id=int(get_id(request.META.get('HTTP_TOKEN'))))
    now = datetime.datetime.now()
    image_list = ''
    record = Record()
    record.user = user
    record.date = now.strftime('%Y-%m-%d')
    record.time = now
    record.image_list = image_list
    record.description = request.POST.get('description')
    record.save()
    image_num = int(request.POST.get('image_num'))
    for i in range(1, image_num + 1):
        record_image = RecordImage()
        record_image.record = record
        image = request.FILES.get(f'image_{i}')
        record_image.image = handle_image(image, os.path.join(RECORD_IMAGE_URL, f'record_{record.id}_image_{i}' +
                                                              os.path.splitext(str(image.name))[1]))
        record_image.save()
        if i == 1:
            image_list += f'{record_image.id}'
        else:
            image_list += f', {record_image.id}'
    record.image_list = image_list
    record.save()
    return JsonResponse({'errno': 0, 'msg': '打卡成功'})


def handle_image(image, path):
    with open('.' + path, 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)
    return path


def record_reminder():
    users = User.objects.all()
    for user in users:
        if len(Record.objects.filter(Q(time__gt=datetime.date.today() - datetime.timedelta(days=1)) &
                                     Q(user=user))) == 0:
            status = sms_sender(
                user.phone,
                1,
                [
                    user.name,
                ]
            )


scheduler.add_job(record_reminder, "cron", hour=18, minute=0, second=0)
# scheduler.start()
