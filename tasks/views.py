from django.shortcuts import render, HttpResponse
import random
import rust.settings as SETTINGS
from utils import *


def run_files(request):
    files = request.POST.get('files', [])
    task_id = "%032x" % random.getrandbits(128)

    for f in files:
        with open("{}/{}/{}".format(SETTINGS.RUST_SRC_PATH, task_id, f.name), 'w+') as src_file:
            src_file.write(f.code)

    result = run(task_id)
    rm_task(task_id)

    return HttpResponse(result)