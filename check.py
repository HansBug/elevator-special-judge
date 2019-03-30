import math
import os
import random
import re


def _parse_input(request):
    pattern = re.compile(r'^\[(\d+\.\d)\](\d+)-FROM-(\d+)-TO-(\d+)$')
    matcher = re.match(pattern, request)
    if not matcher:
        raise ValueError('Invalid Input Form: ' + request)
    time = float(matcher.group(1))
    pid = int(matcher.group(2))
    start = int(matcher.group(3))
    end = int(matcher.group(4))
    return {'time': time, 'pid': pid, 'start': start, 'end': end, 'original': request}


def _check_validity(request_list):
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
        if request['start'] > 15 or request['end'] > 15:
            raise ValueError('Request floor out of range: ' + original)
        if request['start'] == request['end']:
            raise ValueError('Request has same start and end: ' + original)
        if request['time'] < last_time:
            raise ValueError('Request time decreasing: ' + original)
        last_time = request['time']
        pid_dict[request['pid']] = request
        valid_request_count += 1
    if valid_request_count > 30:
        raise ValueError('Too many valid requests')


def _check_time(request_list):
    base_run_timespan = 0.5
    base_serve_timespan = 0.5
    run_timespan_disturb = 0.05
    serve_timespan_disturb = 0.05
    request_time_disturb_upper_bound = 0.1
    request_time_disturb_lower_bound = -0.1
    max_time = 0.0
    for i in range(500):
        run_timespan = base_run_timespan + random.uniform(0, run_timespan_disturb)
        serve_timespan = base_serve_timespan + random.uniform(0, serve_timespan_disturb)
        time = 0.0
        floor = 1
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
            request_start_floor = request['start']
            request_end_floor = request['end']
            if request_time > time:
                time = request_time
            time += run_timespan * abs(request_start_floor - floor)
            floor = request_start_floor
            time += serve_timespan
            time += run_timespan * abs(request_end_floor - floor)
            time += serve_timespan
            floor = request_end_floor
        if time > max_time:
            max_time = time
    if max_time >= 170.0:
        raise ValueError('Request execute time too long')
    return math.ceil(max_time), math.ceil(max(max_time + 5, 1.1 * max_time))


def _check_input_validity(request_list):
    try:
        request_list = [_parse_input(request.rstrip()) for request in request_list]
        _check_validity(request_list)
        time = _check_time(request_list)
        return True, 'Your input is valid, base time is ' + str(time)
    except ValueError as e:
        return False, str(e)


def check(input_file_path):
    input_list = []
    if not os.path.exists(input_file_path):
        raise FileNotFoundError
    with open(input_file_path) as f:
        for line in f:
            input_list.append(line)
        return _check_input_validity(input_list)


if __name__ == '__main__':
    print(check('stdin.txt'))
