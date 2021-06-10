from django.shortcuts import render
# Create your views here.
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from .models import Technician,Vipcard,Class,Classhistory,Coach,Customer,Equipment,Maintenance,Manager,Student
from django.shortcuts import render


@csrf_exempt
def manager_login(request):
    return []

@csrf_exempt
def customer_login(request):
    return  []

@csrf_exempt
def customer_register(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = Customer.objects.get(username=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Customer.DoesNotExist:
        dic['status'] = "Success"
        now = datetime.datetime.now()
        newUser = Customer(username=username, password=password, register_time=now)
        newUser.save()
        return HttpResponse(json.dumps(dic))
    if user is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))
# Create your views here.
