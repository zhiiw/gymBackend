from django.shortcuts import render
from django.db.models import QuerySet
from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from .models import Technician, Vipcard, Class, Classhistory, Coach, Customer, Equipment, Maintenance, Manager, Student
from django.shortcuts import render


@csrf_exempt
def buy_vipcard(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        customer_id = int(post_content['customer_id'])
        deposit = float(post_content['deposit'])
        dic['status'] = "Success"
        customer = Customer.objects.get(id=customer_id)
        customer.membership = "0"

        user = Vipcard.objects.get(customerid=customer)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Vipcard.DoesNotExist:
        dic['status'] = "Success"
        custom = Vipcard(customerid=customer, deposit=deposit)
        custom.save()
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def total_login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    post_content = json.loads(request.body)
    usertype = post_content['usertype']
    if usertype == "Student":
        return login(request)
    if usertype == "Manager":
        return Manager_login(request)

    if usertype == "Technician":
        return technician_login(request)


@csrf_exempt
def buy_class(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        print("ee")
        print(request.body)
        post_content = json.loads(request.body)
        classid = post_content['class_id']
        customer_id = int(post_content['customer_id'])
        coach_id = int(post_content['coach_id'])

        dic['status'] = "Success"
        coach = Coach.objects.get(id=coach_id)
        classes = Class.objects.get(id=classid)

        custom = Student(classid=classes, coach=coach, classleft=customer_id)
        custom.save()
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def get_all_coach(request):
    if request.method != 'GET':
        dic = {}
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    coachs = Coach.objects.all()
    arr = []
    for coach in coachs:
        dic = {}
        dic['coach_name'] = coach.coachname
        dic['coach_id'] = coach.id
        dic['contactnum'] = coach.contactnum
        dic['address'] = coach.address
        dic['speciality'] = coach.speciality
        dic['salary'] = float(coach.salary)

        arr.append(dic)

    dict = {}
    dict['status'] = "Success"
    dict['coach_list'] = arr
    return HttpResponse(json.dumps(dict))


@csrf_exempt
def get_all_technician(request):
    if request.method != 'GET':
        dic = {}
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    technicians = Technician.objects.all()

    arr = []
    for technician in technicians:
        dic = {}
        dic['name'] = technician.name
        dic['id'] = technician.id
        dic['contactnum'] = technician.contactnum
        dic['taddress'] = technician.taddress
        dic['salary'] = float(technician.salary)

        arr.append(dic)

    dict = {}
    dict['status'] = "Success"
    dict['couchs'] = arr
    return HttpResponse(json.dumps(dict))


@csrf_exempt
def create_class(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        classtype = post_content['class_type']
        coach = post_content['coach']
        fee = int(post_content['fee'])
        dic['status'] = "Success"
        custom = Class(coach=coach, fee=fee, classtype=classtype)
        custom.save()
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def Manager_login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = Manager.objects.get(managername=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Manager.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))
    if user.get_matchname() != str(password):
        print(user.get_matchname())
        print(''.join(user.password))
        dic['message'] = "Wrong Password"
        dic['status'] = "Failed"
        return HttpResponse(json.dumps(dic))
    else:
        dic['status'] = "Success"
        dic['user_id'] = user.id
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def technician_login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = Technician.objects.get(name=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Customer.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))
    if user.get_matchname() != str(password):
        print(user.get_matchname())
        print(''.join(user.gender))
        dic['message'] = "Wrong Password"
        dic['status'] = "Failed"
        return HttpResponse(json.dumps(dic))
    else:
        dic['status'] = "Success"
        dic['user_id'] = user.id
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = Customer.objects.get(customername=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Customer.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))
    if user.get_matchname() != str(password):
        print(user.get_matchname())
        print(''.join(user.password))
        dic['message'] = "Wrong Password"
        dic['status'] = "Failed"
        return HttpResponse(json.dumps(dic))
    else:
        dic['status'] = "Success"
        dic['user_id'] = user.id
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def register(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        gender = post_content['gender']
        contactnum = post_content['contact_number']
        user = Customer.objects.get(customername=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Customer.DoesNotExist:
        dic['status'] = "Success"
        now = datetime.datetime.now()
        custom = Customer(customername=username, password=password, gender=gender,
                          contactnum=contactnum)
        custom.save()
        return HttpResponse(json.dumps(dic))
    if user is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def show_all_class(request):
    if request.method != 'GET':
        dic = {}
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    classes = Class.objects.all()
    arr = []
    for ee in classes:
        dic = {}
        dic["class_id"] = ee.id
        dic["fee"] = float(ee.fee)
        dic["coach"] = ee.coach
        dic["classtype"] = ee.classtype
        arr.append(dic)

    dic = {}
    dic['status'] = "Success"
    dic['class_list'] = arr
    return HttpResponse(json.dumps(dic))


@csrf_exempt
def create_Equipment(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['equipname']
        equipdata = post_content['equipdata']
        price = float(post_content['price'])
        lastfix = post_content['lastfix']
        equipment = Equipment.objects.get(customername=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Equipment.DoesNotExist:
        dic['status'] = "Success"
        now = datetime.datetime.now()
        custom = Equipment(equipname=username, equipdata=equipdata, price=price,
                           lastfix=lastfix)
        custom.save()
        return HttpResponse(json.dumps(dic))
    if equipment is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def create_maintaince(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        technician_id = post_content['technician_id']
        equipid = post_content['equipid']
        lastfix = post_content['lastfix']
        equipment = Equipment.objects.get(id=equipid)
        technician = Technician.objects.get(id=technician_id)

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Equipment.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The equipment doesn't exist"
        return HttpResponse(json.dumps(dic))
    except Technician.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The technician doesn't exist"
        return HttpResponse(json.dumps(dic))

    if equipment is not None:
        dic['status'] = "Failed"
        dic['message'] = "equipment exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def delete_student(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        student_id = post_content['student_id']
        stduent = Student.objects.get(id=student_id)
        stduent.delete()
        dic['status'] = "Success"
        dic['message'] = "Student delete sucess"
        return HttpResponse(json.dumps(dic))
    except Student.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The technician doesn't exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def delete_class(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        student_id = post_content['class_id']
        stduent = Class.objects.get(id=student_id)
        stduent.delete()
        dic['status'] = "Success"
        dic['message'] = "Class delete sucess"
        return HttpResponse(json.dumps(dic))
    except Student.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The Class doesn't exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def delete_equipment(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        student_id = post_content['equipment_id']
        stduent = Equipment.objects.get(id=student_id)
        stduent.delete()
        dic['status'] = "Success"
        dic['message'] = "Equipment delete sucess"
        return HttpResponse(json.dumps(dic))
    except Equipment.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The technician doesn't exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def customer_class(request):
    if request.method != 'POST':
        dic = {}
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    post_content = json.loads(request.body)
    student_id = post_content['customer_id']
    stduents = Student.objects.filter(id=student_id)
    arr = []
    for student in stduents:
        dic = {}
        dic["class_id"] = student.classid.id
        dic["fee"] = float(student.classid.fee)
        dic["coach"] = student.classid.coach
        dic["classtype"] = student.classid.classtype
        arr.append(dic)

    dict = {}
    dict['status'] = "Success"
    dict['class_list'] = arr
    return HttpResponse(json.dumps(dict))


@csrf_exempt
def student_get_class(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        student_id = post_content['equipment_id']
        classes_id = post_content['class_id']
        coach_id = post_content['coach_id']
        student_id = post_content['student_id']

        coach = Coach.objects.get(id=coach_id)

        aclass = Classhistory(classid=classes_id, stduentid=student_id, coachid=coach)
        dic['status'] = "Success"
        dic['message'] = "Equipment delete sucess"
        return HttpResponse(json.dumps(dic))
    except Student.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The student doesn,t exist."
        return HttpResponse(json.dumps(dic))
    except Class.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "The class doesn,t exist."
        return HttpResponse(json.dumps(dic))
