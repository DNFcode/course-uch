from django.shortcuts import render, HttpResponse
import random
import rust.settings as SETTINGS
from utils import *
import json
import os
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_files(request):
    files = json.loads(request.POST.get('files', '[]'))
    task_id = "%032x" % random.getrandbits(128)

    if not os.path.exists("{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id)):
        os.makedirs("{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id))

    for name, code in files.items():
        with open("{}/{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id, name), 'w+') as src_file:
            src_file.write(code)

    result = run(task_id)
    rm_task(task_id)

    return HttpResponse(result)


def index(request):
    return render(request, 'task.html')
