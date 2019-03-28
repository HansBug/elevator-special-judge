import re

from model import Passenger


def parse_input(request):
    pattern = re.compile(r'\[\s*(\d+\.\d+)\](\d+)-FROM-(\d+)-TO-(\d+)')
    matcher = re.match(pattern, request)
    if not matcher:
        raise ValueError('Invalid Input')
    time = float(matcher.group(1))
    pid = int(matcher.group(2))
    start = int(matcher.group(3))
    end = int(matcher.group(4))
    return time, Passenger(pid, start, end)


def parse_output(state):
    time_pattern = r'\[\s*(\d+\.\d+)\]'

    def parse_elevator_open(_state):
        pattern = re.compile(time_pattern + r'OPEN-(\d+)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Invalid Elevator OPEN State')
        time = float(matcher.group(1))
        floor = int(matcher.group(2))
        return {'time': time, 'state': 'OPEN', 'floor': floor}

    def parse_elevator_close(_state):
        pattern = re.compile(time_pattern + r'CLOSE-(\d+)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Invalid Elevator CLOSE State')
        time = float(matcher.group(1))
        floor = int(matcher.group(2))
        return {'time': time, 'state': 'CLOSE', 'floor': floor}

    def parse_passenger_in(_state):
        pattern = re.compile(time_pattern + r'IN-(\d+)-(\d+)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Invalid Passenger IN State')
        time = float(matcher.group(1))
        pid = int(matcher.group(2))
        floor = int(matcher.group(3))
        return {'time': time, 'state': 'IN', 'pid': pid, 'floor': floor}

    def parse_passenger_out(_state):
        pattern = re.compile(time_pattern + r'OUT-(\d+)-(\d+)')
        matcher = re.match(pattern, _state)
        if not matcher:
            raise ValueError('Invalid Passenger OUT State')
        time = float(matcher.group(1))
        pid = int(matcher.group(2))
        floor = int(matcher.group(3))
        return {'time': time, 'state': 'OUT', 'pid': pid, 'floor': floor}

    parse_mapper = {
        'OPEN': parse_elevator_open,
        'CLOSE': parse_elevator_close,
        'IN': parse_passenger_in,
        'OUT': parse_passenger_out
    }

    state_keywords = re.findall(r'[A-Z]+', state)
    if not state_keywords or state_keywords[0] not in parse_mapper:
        raise ValueError('Invalid State')
    return parse_mapper[state_keywords[0]](state)


if __name__ == '__main__':
    pass
