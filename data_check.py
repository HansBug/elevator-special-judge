from dcmodule import load_with_args, result_dump

from check import __check_input_validity
from judge import judge, __initialize


def input_check(_stdin):
    return __check_input_validity(_stdin.splitlines())[0]


def output_check(_stdin, _stdout):
    try:
        _, state_list = __initialize(_stdin.splitlines(), _stdout.splitlines())
        if sorted(state_list, key=lambda elem: elem['time']) != state_list:
            raise ValueError('Output not sorted')
    except ValueError:
        return False
    return judge(_stdin.splitlines(), _stdout.splitlines(), decrypted=False)[0]


def data_check(_stdin, _stdout):
    return input_check(_stdin) and output_check(_stdin, _stdout)


if __name__ == "__main__":
    with load_with_args() as _iotuple:
        _stdin, _stdout = _iotuple
        result = data_check(_stdin, _stdout)
        result_dump(result, data={
            "stdin": _stdin,
            "stdout": _stdout,
        })
