from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Label
from .models import User


# 管理员权限，获取所有标签信息
@require_http_methods(["POST"])
@csrf_exempt
def show_labels(request):
    response = {}
    try:
        # 数据库中查询所有标签信息
        labels = Label.objects.filter()
        # 返回json格式标签信息
        response['list'] = json.loads(serializers.serialize("json", labels))
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 管理员权限，向库中添加新标签
@require_http_methods(["POST"])
@csrf_exempt
def add_label(request):
    response = {}
    # 获取前端输入数据
    l = json.loads(request.body)
    try:
        # 向库中增加新的标签信息
        add = Label(name=l['name'], trained=l['trained'], available=l['available'])
        add.save()
        response['msg'] = '添加成功'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 管理员权限，更改标签使用状态
@require_http_methods(["POST"])
@csrf_exempt
def update_use(request):
    response = {}
    # 获取前端输入数据
    up = json.loads(request.body)
    try:
        # 前端请求数据，标签名称
        up_object = Label.objects.get(name=up['name'])
        # 前端请求数据，更改后状态
        up_object.available = up['available']
        up_object.save()
        response['msg'] = '设置成功'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 管理员权限，获取所有用户信息
@require_http_methods(["POST"])
@csrf_exempt
def show_users(request):
    response = {}
    try:
        # 数据库中查找所有用户信息
        users = User.objects.filter()
        # 返回json格式用户信息
        response['list'] = json.loads(serializers.serialize("json", users))
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 测试用api，测试前后端连接情况
@require_http_methods(["POST"])
@csrf_exempt
def test(request):
    tt = json.loads(request.body)
    print("????????????????", tt['type'])
    response = {}
    try:
        response['list'] = json.loads(request.body)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
