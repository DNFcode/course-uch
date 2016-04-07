import subprocess

def run(task_id):
    stdout = subprocess.check_output(['sh', '../rust_init.sh', task_id])
    return stdout


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


def check(task_id):
    task_in = open('../../tests/{}/in'.format(task_id))
    task_out = open('../../tests/{}/out'.format(task_id), 'w+')
    subprocess.call(['sh', '../rust_init.sh', task_id],
                    stdin=task_in, stdout=task_out)

    return compare('../../tests/{}/check'.format(task_id),
                   '../../tests/{}/out'.format(task_id))

print check('1')
