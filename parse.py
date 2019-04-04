import re

from model import Passenger


def parse_input(request):
    pattern = re.compile(r'\[\s*(\d+\.\d+)\](\d+)-FROM-(-?[1-9]\d*)-TO-(-?[1-9]\d*)')
    matcher = re.match(pattern, request)
    if not matcher:
        raise ValueError('Input Format Error | Invalid Input: ' + request)
    time = float(matcher.group(1))
    pid = int(matcher.group(2))
    start = int(matcher.group(3))
    end = int(matcher.group(4))
    return Passenger(pid, start, end, time)


def parse_output(state):
    time_pattern = r'\[\s*(\d+\.\d{4})\]'

    def parse_elevator_open(_state):
        pattern = re.compile(time_pattern + r'OPEN-(-?[1-9]\d*)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Output Format Error | Invalid Elevator OPEN State: ' + _state)
        time = float(matcher.group(1))
        floor = int(matcher.group(2))
        return {'time': time, 'state': 'OPEN', 'floor': floor}

    def parse_elevator_close(_state):
        pattern = re.compile(time_pattern + r'CLOSE-(-?[1-9]\d*)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Output Format Error | Invalid Elevator CLOSE State: ' + _state)
        time = float(matcher.group(1))
        floor = int(matcher.group(2))
        return {'time': time, 'state': 'CLOSE', 'floor': floor}

    def parse_passenger_in(_state):
        pattern = re.compile(time_pattern + r'IN-(\d+)-(-?[1-9]\d*)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Output Format Error | Invalid Passenger IN State: ' + _state)
        time = float(matcher.group(1))
        pid = int(matcher.group(2))
        floor = int(matcher.group(3))
        return {'time': time, 'state': 'IN', 'pid': pid, 'floor': floor}

    def parse_passenger_out(_state):
        pattern = re.compile(time_pattern + r'OUT-(\d+)-(-?[1-9]\d*)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Output Format Error | Invalid Passenger OUT State: ' + _state)
        time = float(matcher.group(1))
        pid = int(matcher.group(2))
        floor = int(matcher.group(3))
        return {'time': time, 'state': 'OUT', 'pid': pid, 'floor': floor}

    def parse_arrive(_state):
        pattern = re.compile(time_pattern + r'ARRIVE-(-?[1-9]\d*)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Output Format Error | Invalid Arrive State: ' + _state)
        time = float(matcher.group(1))
        floor = int(matcher.group(2))
        return {'time': time, 'state': 'ARRIVE', 'floor': floor}

    parse_mapper = {
        'OPEN': parse_elevator_open,
        'CLOSE': parse_elevator_close,
        'IN': parse_passenger_in,
        'OUT': parse_passenger_out,
        'ARRIVE': parse_arrive
    }

    state_keywords = re.findall(r'[A-Z]+', state)
    if not state_keywords or state_keywords[0] not in parse_mapper:
        raise ValueError('Output Format Error | Invalid State: ' + state)
    return parse_mapper[state_keywords[0]](state)


if __name__ == '__main__':
    pass
