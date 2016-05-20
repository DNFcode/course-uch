# coding=utf-8
import subprocess
import rust.settings as SETTINGS
from tasks.models import *


def rm_task(task_id):
    subprocess.call(['sh', './clear.sh', '{}/{}'.format(SETTINGS.RUST_SRC_PATH, task_id)])
    subprocess.call(['sh', './clear.sh', '{}/{}'.format(SETTINGS.RUST_CARGO_PATH, task_id)])
    subprocess.call(['sh', './clear.sh', '{}/{}'.format(SETTINGS.RUST_TESTS_PATH, task_id)])


def compile_rust(task_id):
    try:
        stdout = subprocess.check_output(
            ['sh', './compile.sh', SETTINGS.RUST_CARGO_PATH, SETTINGS.RUST_SRC_PATH, task_id],
            stderr=subprocess.STDOUT)
        return stdout
    except subprocess.CalledProcessError as ex:
        return ex.output


def run(task_id):
    try:
        stdout = subprocess.check_output(
            ['sh', './run_from_file.sh', "{}/{}".format(SETTINGS.RUST_CARGO_PATH, task_id)])
        return stdout
    except subprocess.CalledProcessError as ex:
        return ex.output


def compare(example, result):
    with open(example) as ex, open(result) as res:
        for line in ex:
            if line != res.readline():
                return False
        line = res.readline()
        if not line or line == "\n":
            return True
        else:
            return False


def check_task(task_id, task_db_id):
    checks = Task.objects.filter(task_id=task_db_id)
    for i, condition in enumerate(checks):
        p = subprocess.Popen(
            ['sh', './run.sh', "{}/{}".format(SETTINGS.RUST_CARGO_PATH, task_id)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = p.communicate(input=condition.input)[0].decode()
        if len(stdout) > 0:
            stdout = stdout[:-1] if stdout[-1] == '\n' else stdout
            stdout = stdout[:-1] if stdout[-1] == ' ' else stdout
        output = condition.output.replace('\r', '')
        if stdout != output:
            return u'Не пройден тест №{} из {} тестов.'.format(i+1, len(checks))
    return u'Все тесты пройдены'
