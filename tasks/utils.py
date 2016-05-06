import subprocess
import rust.settings as SETTINGS


def rm_task(task_id):
    subprocess.call(['sh', './clear.sh', '{}/{}'.format(SETTINGS.RUST_SRC_PATH, task_id)])
    subprocess.call(['sh', './clear.sh', '{}/{}'.format(SETTINGS.RUST_CARGO_PATH, task_id)])
    subprocess.call(['sh', './clear.sh', '{}/{}'.format(SETTINGS.RUST_TESTS_PATH, task_id)])


def run(task_id):
    try:
        stdout = subprocess.check_output(
            ['sh', './rust_init.sh', SETTINGS.RUST_CARGO_PATH, SETTINGS.RUST_SRC_PATH, task_id],
            stderr=subprocess.STDOUT)
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


def check(task_id):
    in_path = '{}/{}/in'.format(SETTINGS.RUST_TESTS_PATH, task_id)
    out_path = '{}/{}/out'.format(SETTINGS.RUST_TESTS_PATH, task_id)
    check_path = '{}/{}/check'.format(SETTINGS.RUST_TESTS_PATH, task_id)

    task_in = open(in_path)
    task_out = open(out_path, 'w+')
    subprocess.call(['sh', '../rust_init.sh', task_id],
                    stdin=task_in, stdout=task_out)

    return compare(check_path, out_path)
