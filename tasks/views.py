from django.shortcuts import render, HttpResponse
import random
import rust.settings as SETTINGS
from utils import *
import json
import os
from django.views.decorators.csrf import csrf_exempt


def create_files(files, task_id):
    if not os.path.exists("{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id)):
        os.makedirs("{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id))

    for name, code in files.items():
        folder = os.path.dirname(name)
        if not os.path.exists("{}/{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id, folder)):
            os.makedirs("{}/{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id, folder))
        with open("{}/{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id, name), 'w+') as src_file:
            src_file.write(code)


@csrf_exempt
def run_files(request):
    files = json.loads(request.POST.get('files', '[]'))
    task_id = "%032x" % random.getrandbits(128)

    create_files(files, task_id)

    result = compile_rust(task_id)
    if not result:
        result = run(task_id)

    rm_task(task_id)

    return HttpResponse(result)


@csrf_exempt
def check(request):
    files = json.loads(request.POST.get('files', '[]'))
    bd_task_id = request.POST.get('task_id', '1')
    task_id = "%032x" % random.getrandbits(128)

    create_files(files, task_id)

    result = compile_rust(task_id)
    if not result:
        result = check_task(task_id, bd_task_id)

    rm_task(task_id)

    return HttpResponse(result)


def index(request):
    return render(request, 'task.html')


def t1(request):
    return render(request, 'task1.html')

def t2(request):
    return render(request, 'task2.html')

def t3(request):
    return render(request, 'task3.html')
