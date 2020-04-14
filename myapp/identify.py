from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import cnn.identify as ii

import jieba.analyse


# 为了识别效率，获取文本关键词
def secondary(sentence, k):
    keywords1 = jieba.analyse.extract_tags(sentence, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    keywords2 = jieba.analyse.textrank(sentence, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    res = []
    for item in keywords1[:k]:
        res.append(item[0])
    # 三个关键词用，连接为一个string
    return ', '.join(res)


# 调用cnn类型识别接口，对文本进行标签识别
@require_http_methods(["POST"])
@csrf_exempt
def cnn(request):
    response = {}
    # 从前端获取数据，文本数据text
    text = json.loads(request.body)
    text = text['text']
    try:
        # 调用神经网络识别接口，传入文本数据
        label = ii.cnn_p(text)
        # 识别结果赋值给label
        response['label'] = label
        response['msg'] = '识别成功'
        response['error_num'] = 0
        # 文本三个关键词
        response['secondary'] = secondary(text, 3)
    # 异常处理
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    # 向前端返回数据
    return JsonResponse(response)

