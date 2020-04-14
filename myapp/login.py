from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User


# 系统三个角色对应角色编号
def int_type(s):
    if s == '社交平台':
        return 1
    if s == '广告主':
        return 2
    if s == '管理员':
        return 0


# 返回所有用户数据
@require_http_methods(["POST"])
@csrf_exempt
def show_users(request):
    response = {}
    try:
        # 数据库中查询所有用户数据
        users = User.objects.filter()
        # 以json格式返回用户数据
        response['list'] = json.loads(serializers.serialize("json", users))
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 验证用户登录信息
@require_http_methods(["POST"])
@csrf_exempt
def check(request):
    response = {}
    # 从前端获取数据，用户email，密码和身份
    data = json.loads(request.body)
    try:
        # 数据库中根据用户email和身份查找对应用户
        u = User.objects.filter(email=data['email'], type=int_type(data['type']))
        # 若用户不存在
        if not u:
            # 返回验证信息
            response['msg'] = '用户不存在'
            response['error_num'] = 1
        else:
            # 若密码匹配，则验证错误
            if data['password'] == u[0].password:
                # 返回验证信息
                response['msg'] = '验证成功'
                response['error_num'] = 0
                response['data'] = json.loads(request.body)
                response['id'] = u[0].id
            # 若密码不匹配，则验证失败
            else:
                # 返回验证信息
                response['msg'] = '密码错误'
                response['error_num'] = 2
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
    # 向前端返回验证结果
    return JsonResponse(response)


# 测试用api，测试前后端通信
@require_http_methods(["POST"])
@csrf_exempt
def test(request):
    tt = json.loads(request.body)
    print(tt['type'])
    response = {}
    try:
        response['list'] = json.loads(request.body)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
