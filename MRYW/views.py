from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
import json
import time
from MRYW.models import daily_question

# Create your views here.
person_dic = {
    "a": "admin",
    "b": "admin2",
}

appid = 'wx4e76c2dad14e3341'
secret = 'd5415026ee451dad7fa865da326c1c9a'
QUESTIONS = [
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "Q5",
        "Q6",
        "Q7",
        "Q8",
        "Q9",
        ]

def index(request):
    # print(request)
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
