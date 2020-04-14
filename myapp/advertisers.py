from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Ads
from .models import Like


# 根据广告主id获取对应广告主所有广告数据信息
@require_http_methods(["POST"])
@csrf_exempt
def get_ads_id(request):
    response = {}
    # 从前端获取数据，广告主id
    l = json.loads(request.body)
    idd = l['id']
    try:
        # 从数据库中根据广告主ID查找对应广告数据
        ads = Ads.objects.filter(belong=idd)
        # 以json格式返回广告数据信息
        response['list'] = json.loads(serializers.serialize("json", ads))
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 根据广告id删除对应广告
@require_http_methods(["POST"])
@csrf_exempt
def delete_ads(request):
    response = {}
    # 从前端获取数据，广告id
    l = json.loads(request.body)
    idd = l['id']
    try:
        # 从数据库中删除对应id的广告数据
        ads = Ads.objects.get(id=idd)
        ads.delete()
        # 返回处理结果
        response['msg'] = '删除成功'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回结果
    return JsonResponse(response)


# 广告主添加新广告
@require_http_methods(["POST"])
@csrf_exempt
def add_ads(request):
    response = {}
    # 从前端回去广告数据
    l = json.loads(request.body)
    try:
        # name：广告名称
        # text：广告文本
        # belong：所属广告公司id
        # label：广告一级标签
        # secondary1 2 3：广告三个关键词
        add = Ads(name=l['name'], text=l['text'], belong=l['belong'], label=l['label'], pv=0,
                  secondary1=l['secondary1'], secondary2=l['secondary2'], secondary3=l['secondary3'])
        # 数据库中添加对应广告数据
        add.save()
        # 返回处理结果
        response['msg'] = '添加成功'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回处理结果
    return JsonResponse(response)


# 获取所有广告数据
@require_http_methods(["POST"])
@csrf_exempt
def get_ads(request):
    response = {}
    try:
        # 数据库中查询所有广告数据
        ads = Ads.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", ads))
        # 返回处理结果
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)


# 更新广告点击量
# 前端点击查看广告即该广告点击量加1
@require_http_methods(["POST"])
@csrf_exempt
def update_pv(request):
    response = {}
    # 获取前端数据，广告id
    up = json.loads(request.body)
    try:
        # 数据库中根据广告id查询广告数据
        up_object = Ads.objects.get(id=up['ads_id'])
        # 对应广告点击量+1
        up_object.pv += 1
        # 更新后结果存入数据库
        up_object.save()
        # 返回处理结果
        response['msg'] = '设置成功'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回处理结果
    return JsonResponse(response)


# 添加用户-广告点赞
# 用户对对应广告点击喜欢，即添加一对用户-广告点赞数据
@require_http_methods(["POST"])
@csrf_exempt
def add_like(request):
    response = {}
    # 获取前端数据，用户id，广告id
    l = json.loads(request.body)
    try:
        # 查询数据库like中是否有该用户-广告点赞对
        u = Like.objects.filter(cust_id=l['cust_id'], ads_id=l['ads_id'])
        up_object = Ads.objects.get(id=l['ads_id'])
        up_object.pv += 1
        up_object.save()
        # 若库中没有该用户-广告点赞对
        # 数据库中like增加一对用户-广告
        if not u:
            add = Like(cust_id=l['cust_id'], ads_id=l['ads_id'], weight=1)
            add.save()
            response['msg'] = '添加成功'
            response['error_num'] = 0
        # 若库中有该用户-广告点赞对
        # 该用户-广告点赞对权重+1
        else:
            u[0].weight += 1
            u[0].save()
            response['msg'] = '更新成功'
            response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回处理结果
    return JsonResponse(response)
