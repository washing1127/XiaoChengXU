from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
import json
import time
from MRYW.models import daily_question
import requests

import requests

# Create your views here.
person_dic = {
    "backpack": "娇娇",
    "wxx": "王小许",
    "huyajie": "胡亚捷",
    "baimingtai": "白明泰",
    "zyx20041026": "张瑜璇",
    "kxz1823115435": "孔祥壮",
    "yy": "闫毅",
    "zhs": "张海生",
}

appid = 'wx4e76c2dad14e3341'
secret = 'd5415026ee451dad7fa865da326c1c9a'

QUESTIONS = [
        "我今天是否完成了自己的小目标",
        "今天有哪些事可以让我得到成长",
        "今天有哪些地方我做得还不够好",
        "我人生的终极目标是什么",
        "我明天的小目标是什么",
        "有哪些想对自己说的话",
        ]

def index(request):
    print("in request")
    person_id = request.GET.get('person_id')
    print(person_id, "person_id")
    if person_id not in person_dic.keys():
        res = '{"status": 0}'
    else:
        dic = {"status": 1}
        dic["QUESTIONS"] = ",".join(QUESTIONS)
        name = person_dic[person_id]
        date = time.strftime("%Y-%m-%d")
        print(name)
        print(date)
        today_data = daily_question.objects.filter(Q(name=name) & Q(date=date))
        print(today_data)
        if today_data:
            all_data = daily_question.objects.filter(name=name)
            dic["today_done"] = "true"
            ret_list = []
            for i in all_data:
                data = i.data
                date = i.date
                data = json.loads(data)
                data["date"] = date
                ret_list.append(json.dumps(data))
            dic["data"] = ret_list
        else:
            dic["appid"] = appid
            dic["secret"] = secret
            dic["today_done"] = ""
            dic["data"] = []
        res = json.dumps(dic)
        return HttpResponse(res)

    return HttpResponse(res)


def create(request):

    if request.method == "POST":
        data = request.body.decode("utf-8")
        # print("data:", data)
        # print(type(data))
        # print(str(data))
        secret_key = json.loads(data)["person_id"]
        if secret_key not in person_dic.keys():
            return HttpResponse("没有找到该用户")
        # print("post data:", request.body)
        # print(type(request.body))
        # print(str(request.body))
        q = daily_question()
        q.name = person_dic[secret_key]
        q.data = data
        q.date = time.strftime("%Y-%m-%d")
        q.save()
        all_data = daily_question.objects.filter(name=person_dic[secret_key])
        # print(all_data)
        # print(type(all_data))
        ret_list = []
        for i in all_data:
            data = i.data
            date = i.date
            data = json.loads(data)
            data["date"] = date
            ret_list.append(json.dumps(data))
        dic = {"status": 1}
        dic["data"] = ret_list
        s = json.dumps(dic)

        return HttpResponse(s)


def login(request):
    res_code = request.GET.get('res_code')
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={res_code}&grant_type=authorization_code'
    resp = requests.get(url)
    # <<<<<<< HEAD
    # resp.status_code
    # =======

    # >>>>>>> 07241125cf06cd0067f8bf8acac8736a9af92141
    ret = resp.text

    return HttpResponse(ret)
