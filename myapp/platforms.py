from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os
import cnn.identify as ii

from .models import Customers
from .models import Words

import jieba.analyse


def secondary(sentence, k):
    keywords1 = jieba.analyse.extract_tags(sentence, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    keywords2 = jieba.analyse.textrank(sentence, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    res = []
    for item in keywords1[:k]:
        res.append(item[0])
    return res


def add_file(name, text, belong):
    u = Customers.objects.filter(name=name)
    if not u:
        add_c = Customers(name=name, belong=belong)
        add_c.save()

    u = Customers.objects.get(name=name)
    cust_id = u.id
    label = ii.cnn_p(text)
    second = secondary(text, 3)
    add_w = Words(text=text, belong=cust_id, label=label,
                secondary1=second[0], secondary2=second[1], secondary3=second[2])
    add_w.save()


@require_http_methods(["POST"])
@csrf_exempt
def add_cust(request):
    response = {}
    l = json.loads(request.body)
    try:
        add = Customers(name=l['name'], belong=l['belong'])
        add.save()
        response['msg'] = '添加成功'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
@csrf_exempt
def get_cust(request):
    response = {}
    try:
        cust = Customers.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", cust))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
@csrf_exempt
def add_words(request):
    response = {}
    l = json.loads(request.body)
    try:
        add = Words(text=l['text'], belong=l['belong'], label=l['label'],
                    secondary1=l['secondary1'], secondary2=l['secondary2'], secondary3=l['secondary3'])
        add.save()
        response['msg'] = '添加成功'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
@csrf_exempt
def update_label(request):
    response = {}
    try:
        l = json.loads(request.body)
        id = l['id']
        cust = Customers.objects.get(id=id)
        cust.label1 = l['label1']
        cust.label2 = l['label2']
        cust.label3 = l['label3']
        cust.save()
        response['??'] = l['label1']
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
@csrf_exempt
def upload_cust(request):
    response = {}
    try:
        print("!!!!!!!!!!!!!!!!")
        if request.FILES:
            myFile = None
            for i in request.FILES:
                myFile = request.FILES[i]
            if myFile:
                # dir = os.path.join(os.path.join('file', 'static'), 'profiles')
                dir = '/Users/yukang/Desktop/Django-2.2.5/testdj/myapp/file'
                destination = open(os.path.join(dir, myFile.name),
                                   'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
            print("???????", dir, destination)
            f = open(dir + '/' + myFile.name, 'r')
            belong = request.POST['belong']
            print("~~~~~~~~")
            cont = f.readline()
            name, text = cont.split('\t')[0], cont.split('\t')[1]
            while cont:
                add_file(name, text, belong)
                cont = f.readline()
                name, text = cont.split('\t')[0], cont.split('\t')[1]
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(str(e))
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)



