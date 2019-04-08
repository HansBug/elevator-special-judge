import copy
import os
import random
import re

import math


def __parse_input(request):
    pattern = re.compile(r'^\[(\d+\.\d)\](\d+)-FROM-(-?[1-9]\d*)-TO-(-?[1-9]\d*)$')
    matcher = re.match(pattern, request)
    if not matcher:
        raise ValueError('Invalid Input Form: ' + request)
    time = float(matcher.group(1))
    pid = int(matcher.group(2))
    start = int(matcher.group(3))
    end = int(matcher.group(4))
    return {'time': time, 'pid': pid, 'start': start, 'end': end, 'served': False, 'original': request}


def __check_validity(request_list):
    last_time = 0.0
    valid_request_count = 0
    pid_dict = {}
    for request in request_list:
        original = request['original']
        if request['time'] < 0.0:
            raise ValueError('Request time negative: ' + original)
        if request['pid'] in pid_dict:
            raise ValueError('Request pid repeated: ' + original)
        if request['pid'] < 0 or request['pid'] > 2147483647:
            raise ValueError('Request pid out pf range: ' + original)
        if request['start'] < -3 or request['start'] > 16 or request['end'] < -3 or request['end'] > 16:
            raise ValueError('Request floor out of range: ' + original)
        if request['start'] == 0 or request['end'] == 0:
            raise ValueError('Request floor cannot be zero')
        if request['start'] == request['end']:
            raise ValueError('Request has same start and end: ' + original)
        if request['time'] < last_time:
            raise ValueError('Request time decreasing: ' + original)
        last_time = request['time']
        pid_dict[request['pid']] = request
        valid_request_count += 1
    if valid_request_count < 1:
        raise ValueError("There is no valid request")
    if valid_request_count > 30:
        raise ValueError('Too many valid requests')


base_run_timespan = 0.4
base_serve_timespan = 0.4
run_timespan_disturb = 0.04
serve_timespan_disturb = 0.04
request_time_disturb_upper_bound = 0.1
request_time_disturb_lower_bound = -0.1
basement_floor_count = 3


def __simulate(request_list, run_timespan, serve_timespan):
    # pre-treat requests: reset request time and add floor count to basement floors
    last_request_random_time = 0.0
    for index, request in enumerate(request_list):
        request_real_time = request['time']
        request_random_disturb = random.uniform(request_time_disturb_upper_bound, request_time_disturb_lower_bound)
        if index == 0:
            request_time = max(0, request_real_time + request_random_disturb)
        else:
            request_time = max(
                max(last_request_random_time, request_real_time) + request_random_disturb,
                last_request_random_time)
        last_request_random_time = request_time
        request['time'] = request_time
        if request['start'] < 0:
            request['start'] += 1
        if request['end'] < 0:
            request['end'] += 1
        request['start'] += basement_floor_count - 1
        request['end'] += basement_floor_count - 1

    pickup_request_bundle = []
    last_request_finish_time = 0.0
    floor = basement_floor_count

    def __build_basic_time(_time, _start, _end):
        base_time = _time + serve_timespan + run_timespan * abs(_start - floor)
        floor_time_checkpoints[_start]['served'] = True
        floor_time_checkpoints[_start]['time'] = base_time
        for i in range(_start, _end, int(math.copysign(1, _end - _start))):
            floor_time_checkpoints[i]['time'] = base_time + run_timespan * abs(i - _start)
        floor_time_checkpoints[_end]['served'] = True
        floor_time_checkpoints[_end]['time'] = base_time + run_timespan * abs(_end - _start) + serve_timespan

    def __update_pickup_time(_start, _end, _travel_end):
        direction = int(math.copysign(1, _end - _start))
        base_update_time = floor_time_checkpoints[_travel_end]['time']
        for i in range(_travel_end, _end + direction, direction):
            if i != _travel_end:
                base_update_time += run_timespan
                floor_time_checkpoints[i]['time'] = base_update_time
        base_update_time = 0.0
        if not floor_time_checkpoints[_start]['served']:
            base_update_time += serve_timespan
            floor_time_checkpoints[_start]['served'] = True
        for i in range(_start, _end + direction, direction):
            floor_time_checkpoints[i]['time'] += base_update_time
        if not floor_time_checkpoints[_end]['served']:
            base_update_time += serve_timespan
            floor_time_checkpoints[_end]['served'] = True
        for i in range(_end, _travel_end + direction, direction):
            floor_time_checkpoints[i]['time'] += base_update_time
        if _start < _end < _travel_end or _travel_end < _end < _start:
            if not floor_time_checkpoints[_travel_end]['served']:
                floor_time_checkpoints[_travel_end]['served'] = True
                floor_time_checkpoints[_travel_end]['time'] += serve_timespan

    while not all([request['served'] for request in request_list]):
        floor_time_checkpoints = [{'served': False, 'time': 0.0} for i in range(19)]
        if pickup_request_bundle:
            main_request = pickup_request_bundle.pop(0)
            pickup_request_bundle = []
        else:
            main_request = next(request for request in request_list if not request['served'])
        time = max(last_request_finish_time, main_request['time'])
        start = main_request['start']
        end = main_request['end']
        __build_basic_time(time, start, end)
        travel_end = end
        while True:
            next_pickup_request = next((request for request in request_list
                                        if not request['served'] and
                                        request not in pickup_request_bundle and
                                        request is not main_request and
                                        min(start, end) <= request['start'] <= max(start, end) and
                                        (end - start) * (request['end'] - request['start']) > 0 and
                                        request['time'] <= floor_time_checkpoints[request['start']]['time']), None)
            if not next_pickup_request:
                break
            __update_pickup_time(next_pickup_request['start'], next_pickup_request['end'], travel_end)
            travel_end = max(travel_end, next_pickup_request['end']) if end > start \
                else min(travel_end, next_pickup_request['end'])
            pickup_request_bundle.append(next_pickup_request)
        for request in pickup_request_bundle:
            if min(start, end) <= request['start'] <= max(start, end):
                request['served'] = True
        pickup_request_bundle = [request for request in pickup_request_bundle if not request['served']]
        main_request['served'] = True
        last_request_finish_time = floor_time_checkpoints[travel_end]['time']
        floor = travel_end

    time = last_request_finish_time
    return time


def __calculate_time(request_list):
    max_time = 0.0
    for i in range(5000):
        run_timespan = base_run_timespan + random.uniform(0, run_timespan_disturb)
        serve_timespan = base_serve_timespan + random.uniform(0, serve_timespan_disturb)
        time = __simulate(copy.deepcopy(request_list), run_timespan, serve_timespan)
        if time > max_time:
            max_time = time
    # return max_time, max(max_time + 3, 1.05 * max_time)
    return math.ceil(max_time), math.ceil(max(max_time + 3, 1.05 * max_time))


def __parse_request_list(input_list):
    return [__parse_input(request.rstrip()) for request in input_list]


def __check_input_validity(input_list):
    try:
        request_list = __parse_request_list(input_list)
        __check_validity(request_list)
        base_time, max_time = __calculate_time(request_list)
        if base_time >= 170.0:
            raise ValueError('Request execute time too long')
        return True, 'Your input is valid, base time is ' + str(base_time) + ', max time is ' + str(max_time)
    except ValueError as e:
        return False, str(e)


def get_base_and_max_time(input_list):
    request_list = __parse_request_list(input_list)
    return __calculate_time(request_list)


def check(input_file_path):
    input_list = []
    if not os.path.exists(input_file_path):
        raise FileNotFoundError
    with open(input_file_path) as f:
        for line in f:
            input_list.append(line)
        return __check_input_validity(input_list)


if __name__ == '__main__':
    print(check('stdin.txt'))
