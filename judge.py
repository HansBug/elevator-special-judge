import json
import re

from aes import decrypt
from model import Elevator
from parse import parse_input, parse_output

ACCEPTED = 'Your answer is correct'
WRONG_ANSWER = 'Your answer does not meet the final requirements.' \
               'Some passengers are still in the elevator or not arrived at their target floor yet.' \
               'Or maybe the elevator\'s door is not closed.'


def decrypt_aes(encrypted, do_it=False):
    if do_it:
        try:
            pattern = re.compile(r'\[\s*\d+\.\d+\](.*)')
            matcher = re.match(pattern, encrypted)
            cipher = matcher.group(1)
            plain = decrypt(cipher)
            plain_json = json.loads(plain)
            return plain_json['content']
        except Exception:
            raise ValueError('Unexpected encryption error occurred. '
                             'If you are not trying to hack the judge system, '
                             'please contact the course staff for a solution.')
    else:
        return encrypted


def _initialize(input_list, output_list):
    output_list = [decrypt_aes(output_line) for output_line in output_list]
    passenger_list = [parse_input(request) for request in input_list]
    state_list = [parse_output(state) for state in output_list]
    # passenger_list.sort(key=lambda e: e['time']) 暂时用不到，不过之后也许会用到
    # state_list.sort(key=lambda e: e['time']) 输入数据确保时间单调不递减，暂时用不到
    passenger_dict = {passenger[1].pid: passenger[1] for passenger in passenger_list}
    return passenger_dict, state_list


def _simulate_elevator_open(**kwargs):
    elevator = kwargs['elevator']
    state = kwargs['state']
    time = state['time']
    floor = state['floor']
    elevator.open(floor, time)


def _simulate_elevator_close(**kwargs):
    elevator = kwargs['elevator']
    state = kwargs['state']
    time = state['time']
    floor = state['floor']
    elevator.close(floor, time)


def _simulate_passenger_in(**kwargs):
    elevator = kwargs['elevator']
    passenger_dict = kwargs['passenger_dict']
    state = kwargs['state']
    time = state['time']
    pid = state['pid']
    floor = state['floor']
    if pid not in passenger_dict:
        raise ValueError(' '.join([
            'Passenger',
            str(pid),
            'cannot enter the elevator',
            'because he/she does not exist'
        ]))
    passenger = passenger_dict[pid]
    elevator.enter_passenger(passenger, floor, time)


def _simulate_passenger_out(**kwargs):
    elevator = kwargs['elevator']
    passenger_dict = kwargs['passenger_dict']
    state = kwargs['state']
    time = state['time']
    pid = state['pid']
    floor = state['floor']
    if pid not in passenger_dict:
        raise ValueError(' '.join([
            'Passenger',
            str(pid),
            'cannot leave the elevator',
            'because he/she does not exist'
        ]))
    passenger = passenger_dict[pid]
    elevator.leave_passenger(passenger, floor, time)


def judge(input_list, output_list):
    elevator = Elevator()
    try:
        passenger_dict, state_list = _initialize(input_list, output_list)
    except ValueError as e:
        return False, str(e)
    simulate_mapper = {
        'OPEN': _simulate_elevator_open,
        'CLOSE': _simulate_elevator_close,
        'IN': _simulate_passenger_in,
        'OUT': _simulate_passenger_out
    }
    for state in state_list:
        try:
            simulate_mapper[state['state']](
                elevator=elevator,
                state=state,
                passenger_dict=passenger_dict,
            )
        except ValueError as e:
            return False, str(e)
    return (True, ACCEPTED) if \
        not elevator.serving() and all([True if
                                        not passenger.in_elevator and passenger.floor == passenger.target
                                        else False
                                        for passenger in passenger_dict.values()]) \
        else (False, WRONG_ANSWER)


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
    result = judge(_input, _output)
    print(result)
