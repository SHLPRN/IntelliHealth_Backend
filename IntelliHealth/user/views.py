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
    record = Record()
    record.user = user
    record.date = now.strftime('%Y-%m-%d')
    record.time = now
    description = request.POST.get('description')
    if description is None or description == '':
        description = '暂无打卡说明'
    record.description = description
    record.save()
    image_num = int(request.POST.get('image_num'))
    for i in range(1, image_num + 1):
        record_image = RecordImage()
        record_image.record = record
        image = request.FILES.get(f'image_{i}')
        record_image.image = handle_image(image, os.path.join(RECORD_IMAGE_URL, f'record_{record.id}_image_{i}' +
                                                              os.path.splitext(str(image.name))[1]))
        record_image.save()
    return JsonResponse({'errno': 0, 'msg': '打卡成功'})


@csrf_exempt
def search_record(request):
    user = User.objects.get(id=int(get_id(request.META.get('HTTP_TOKEN'))))
    date = request.POST.get('date')
    records = Record.objects.filter(Q(user=user) & Q(date=date)).order_by('-time')
    record_num = len(records)
    data = [
        {
            'id': record.id,
            'time': record.time.strftime('%Y-%m-%d %H:%M:%S'),
            'description': record.description,
            'image_list': [
                record_image.image for record_image in RecordImage.objects.filter(record=record)
            ]
        } for record in records
    ]
    return JsonResponse({'errno': 0, 'record_num': record_num, 'data': data})


@csrf_exempt
def get_weekly_record(request):
    user = User.objects.get(id=int(get_id(request.META.get('HTTP_TOKEN'))))
    records = Record.objects.filter(Q(time__gt=datetime.date.today() - datetime.timedelta(days=7)) &
                                    Q(user=user)).order_by('-time')
    record_num = len(records)
    mid_data = {}
    date_list = []
    for record in records:
        if record.date in mid_data:
            mid_data[record.date]['num'] += 1
            mid_data[record.date]['record_list'].append({
                'id': record.id,
                'time': record.time.strftime('%Y-%m-%d %H:%M:%S'),
                'description': record.description,
                'image_list': [
                    record_image.image for record_image in RecordImage.objects.filter(record=record)
                ]
            })
        else:
            date_list.append(record.date)
            mid_data[record.date] = {
                'date': record.date,
                'num': 1,
                'record_list': [
                    {
                        'id': record.id,
                        'time': record.time.strftime('%Y-%m-%d %H:%M:%S'),
                        'description': record.description,
                        'image_list': [
                            record_image.image for record_image in RecordImage.objects.filter(record=record)
                        ]
                    }
                ]
            }
    data = [
        mid_data[date] for date in date_list
    ]
    return JsonResponse({'errno': 0, 'record_num': record_num, 'data': data})


@csrf_exempt
def get_other_record(request):
    users = User.objects.all()
    data = []
    for user in users:
        records = Record.objects.filter(Q(time__gt=datetime.date.today() - datetime.timedelta(days=3)) &
                                        Q(user=user)).order_by('-time')
        record_num = len(records)
        mid_data = {}
        date_list = []
        for record in records:
            if record.date in mid_data:
                mid_data[record.date]['num'] += 1
                mid_data[record.date]['record_list'].append({
                    'id': record.id,
                    'time': record.time.strftime('%Y-%m-%d %H:%M:%S'),
                    'description': record.description,
                    'image_list': [
                        record_image.image for record_image in RecordImage.objects.filter(record=record)
                    ]
                })
            else:
                date_list.append(record.date)
                mid_data[record.date] = {
                    'date': record.date,
                    'num': 1,
                    'record_list': [
                        {
                            'id': record.id,
                            'time': record.time.strftime('%Y-%m-%d %H:%M:%S'),
                            'description': record.description,
                            'image_list': [
                                record_image.image for record_image in RecordImage.objects.filter(record=record)
                            ]
                        }
                    ]
                }
        data.append({
            'name': user.name,
            'nickname': user.nickname,
            'record_num': record_num,
            'data': [
                mid_data[date] for date in date_list
            ]
        })
    return JsonResponse({'errno': 0, 'data': data})


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
scheduler.start()
