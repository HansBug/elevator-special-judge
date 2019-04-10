import json
import re

from aes import decrypt
from check import get_base_and_max_time
from model import Elevator
from parse import parse_input, parse_output

ACCEPTED = 'Accepted | Your answer is correct'
WRONG_ANSWER = 'Wrong Answer | '
TIME_LIMIT_EXCEEDED = 'Time Limit Exceeded | Your program exceeded max time limit.'


def __decrypt_aes(encrypted):
    pattern = re.compile(r'^\[\s*\d+\.\d+\](.*)')
    matcher = re.match(pattern, encrypted)
    cipher = matcher.group(1)
    try:
        plain = decrypt(cipher)
        plain_json = json.loads(plain)
        return plain_json['content']
    except Exception:
        raise ValueError('Encryption Error | Unexpected encryption error occurred. '
                         'You might have printed some redundant outputs to stdout. '
                         'Please make sure that all your outputs are printed by TimableOutput.')


def __check_state_list_validity(state_list):
    for state in state_list:
        if not (-3 <= state['floor'] <= -1 or 1 <= state['floor'] <= 16):
            raise ValueError(' '.join([
                'Wrong State |'
                'There is no floor',
                str(state['floor'])]))


def __initialize(input_list, output_list):
    passenger_list = [parse_input(request) for request in input_list]
    state_list = [parse_output(state) for state in output_list]
    # passenger_list.sort(key=lambda e: e['time']) 暂时用不到，不过之后也许会用到
    # state_list.sort(key=lambda e: e['time']) 输出数据确保时间单调不递减，暂时用不到
    passenger_dict = {passenger.pid: passenger for passenger in passenger_list}
    __check_state_list_validity(state_list)
    return passenger_dict, state_list


def __simulate_elevator_arrive(**kwargs):
    elevator = kwargs['elevator']
    state = kwargs['state']
    time = state['time']
    floor = state['floor']
    elevator.arrive(floor, time)


def __simulate_elevator_open(**kwargs):
    elevator = kwargs['elevator']
    state = kwargs['state']
    time = state['time']
    floor = state['floor']
    elevator.open(floor, time)


def __simulate_elevator_close(**kwargs):
    elevator = kwargs['elevator']
    state = kwargs['state']
    time = state['time']
    floor = state['floor']
    elevator.close(floor, time)


def __simulate_passenger_in(**kwargs):
    elevator = kwargs['elevator']
    passenger_dict = kwargs['passenger_dict']
    state = kwargs['state']
    time = state['time']
    pid = state['pid']
    floor = state['floor']
    if pid not in passenger_dict:
        raise ValueError(' '.join([
            'Wrong State |',
            'Passenger',
            str(pid),
            'cannot enter the elevator',
            'because he/she does not exist'
        ]))
    passenger = passenger_dict[pid]
    elevator.enter_passenger(passenger, floor, time)


def __simulate_passenger_out(**kwargs):
    elevator = kwargs['elevator']
    passenger_dict = kwargs['passenger_dict']
    state = kwargs['state']
    time = state['time']
    pid = state['pid']
    floor = state['floor']
    if pid not in passenger_dict:
        raise ValueError(' '.join([
            'Wrong State |',
            'Passenger',
            str(pid),
            'cannot leave the elevator',
            'because he/she does not exist'
        ]))
    passenger = passenger_dict[pid]
    elevator.leave_passenger(passenger, floor, time)


def judge(input_list, output_list, check_max_time=False, decrypted=True):
    base_time, max_time = get_base_and_max_time(input_list)
    elevator = Elevator()
    try:
        if decrypted:
            output_list = list(map(__decrypt_aes, output_list))
        passenger_dict, state_list = __initialize(input_list, output_list)
    except ValueError as e:
        return False, str(e), output_list, 0
    state_list.sort(key=lambda elem: elem['time'])
    output_list.sort(key=lambda elem: float(re.findall(r'\[\s*(\d+\.\d{4})\]', elem)[0]))
    simulate_mapper = {
        'OPEN': __simulate_elevator_open,
        'CLOSE': __simulate_elevator_close,
        'IN': __simulate_passenger_in,
        'OUT': __simulate_passenger_out,
        'ARRIVE': __simulate_elevator_arrive
    }
    for state in state_list:
        try:
            simulate_mapper[state['state']](
                elevator=elevator,
                state=state,
                passenger_dict=passenger_dict,
            )
        except ValueError as e:
            return False, str(e), output_list, 0
    if elevator.time > (max_time if check_max_time else 200.0):
        return False, TIME_LIMIT_EXCEEDED, output_list, 0
    if elevator.serving():
        return False, WRONG_ANSWER + 'Your elevator\'s door is not closed', output_list, 0
    for passenger in passenger_dict.values():
        if passenger.in_elevator:
            return False, WRONG_ANSWER + 'Passenger ' + str(passenger.pid) + ' is still in the elevator', output_list, 0
        if passenger.floor != passenger.target:
            return False, WRONG_ANSWER + 'Passenger ' + \
                   str(passenger.pid) + ' has not arrived at his/her target floor yet', output_list, 0
    return True, ACCEPTED, output_list, elevator.time


def open_file(input_file, output_file):
    input_list = []
    output_list = []
    with open(input_file) as _input_file:
        for _input_line in _input_file:
            input_list.append(_input_line.strip())
    with open(output_file) as _output_file:
        for _output_line in _output_file:
            output_list.append(_output_line.strip())
    return input_list, output_list


if __name__ == '__main__':
    input_file_path = 'stdin.txt'
    output_file_path = 'stdout.txt'
    _input, _output = open_file(input_file_path, output_file_path)
    result = judge(_input, _output, decrypted=False)
    print(result)
