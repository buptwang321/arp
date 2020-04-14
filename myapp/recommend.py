from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from bert_serving.client import BertClient
import numpy as np

from .models import Words
from .models import Ads


# 余弦相似度计算
def cos_sim(vector_a, vector_b):
    # 计算向量a，b
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    #返回余弦相似度结果
    return sim


# 用户标签按照权重排列并返回top-n
def top_label(label):
    # 存储标签-权重
    count = dict()
    # 计算每个标签权重
    for l in label:
        count[l] = count.get(l, 0) + 1
    # 排序
    list = sorted(count.items(), key=lambda x: x[1])
    res = []
    # 将最高三个作为结果返回
    for item in list[:3]:
        res.append(item[0])
    print(res)
    # 返回权重最高的三个标签
    return res


# 广告推荐
def top_ads(ads, ss):
    # 启动bert服务
    bc = BertClient()
    count = dict()
    temp = [ss]
    # 对每个广告，获取计算其关键词，并bert词向量
    for item in ads:
        secondary = item.secondary1 + item.secondary2 + item.secondary3
        temp.append(secondary)
    # 计算bert词向量
    bert = bc.encode(temp)
    user = bert[0]
    print("???????", temp)
    # 对用户偏好向量和广告关键词向量计算余弦相似度
    for i, item in enumerate(ads):
        count[item] = cos_sim(user, bert[i+1])
    # 进行排序
    sorted_list = sorted(count.items(), key=lambda x: x[1])
    res = []
    # 返回推荐结果
    for item in sorted_list[:5]:
        # 可规定推荐结果相似度下限
        # if item[1] >= 0.95:
        res.append(item[0])
    print(sorted_list, '!!!!!!', res)
    # 返回广告推荐数据
    return res


# 根据用户id获取其兴趣标签
@require_http_methods(["POST"])
@csrf_exempt
def get_label(request):
    response = {}
    # 从前端获取请求数据，用户id
    l = json.loads(request.body)
    id = l['id']
    try:
        # 数据库中根据用户id获取其发表过的文本数据
        words = Words.objects.filter(belong=id)
        labels = []
        # 将所有文本的标签存入labels
        for item in words:
            labels.append(item.label)
        # 计算权重，取top-3
        label = top_label(labels)
        # 返回计算结果
        response['label'] = label
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回计算结果
    return JsonResponse(response)


# 向用户进行广告推荐
@require_http_methods(["POST"])
@csrf_exempt
def get_recommend(request):
    response = {}
    # 从前端获取请求数据，用户id
    l = json.loads(request.body)
    id = l['id']
    try:
        # 数据库中根据用户id获取其发表过的文本数据
        words = Words.objects.filter(belong=id)
        labels = []
        ss = ''
        # labels存储标签
        # ss存储每条文本关键词
        for item in words:
            labels.append(item.label)
            ss += item.secondary1 + item.secondary2 + item.secondary3
        # 计算标签权重，取top-3
        label = top_label(labels)
        # 在广告数据库中，根据label筛选广告
        ads = Ads.objects.filter(label__in=label)
        # 通过bert词向量计算，进行广告推荐
        res = top_ads(ads, ss)
        # 返回计算结果
        response['res'] = json.loads(serializers.serialize("json", res))
        response['msg'] = 'success'
        response['error_num'] = 0
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回计算结果
    return JsonResponse(response)


