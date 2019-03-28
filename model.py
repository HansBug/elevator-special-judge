from enum import Enum, unique


class Passenger:
    def __init__(self, pid, start, target):
        self._pid = pid
        self._floor = start
        self._target = target
        self._in_elevator = False

    @property
    def pid(self):
        return self._pid

    @property
    def floor(self):
        return self._floor

    @property
    def target(self):
        return self._target

    @property
    def in_elevator(self):
        return self._in_elevator

    def enter_elevator(self, enter_floor):
        if self._in_elevator:
            raise ValueError(' '.join([
                'Passenger',
                str(self._pid),
                'cannot enter the elevator twice at floor',
                str(enter_floor)
            ]))
        if self._floor != enter_floor:
            raise ValueError(' '.join([
                'Passenger',
                str(self._pid),
                'cannot enter the elevator',
                'at another floor'
            ]))
        self._floor = enter_floor
        self._in_elevator = True

    def leave_elevator(self, leave_floor):
        if not self._in_elevator:
            raise ValueError(' '.join([
                'Passenger',
                str(self._pid),
                'cannot leave the elevator twice at floor',
                str(leave_floor)
            ]))
        self._floor = leave_floor
        self._in_elevator = False


class Elevator:
    run_timespan = 0.5
    serve_timespan = 0.5

    @unique
    class State(Enum):
        STOPPED = 0,
        RUNNING = 1,
        SERVING = 2

    def __init__(self):
        self._floor = 1
        self._time = 0.0
        self._state = Elevator.State.STOPPED
        self._passengers = {}

    @property
    def floor(self):
        return self._floor

    @property
    def time(self):
        return self._time

    @property
    def state(self):
        return self._state

    def enter_passenger(self, passenger, floor, time):
        if passenger.pid in self._passengers:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'already in elevator',
                'so he/she cannot get in'
            ]))
        if self._state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot enter elevator',
                'when elevator is not serving'
            ]))
        if floor != self._floor:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot enter elevator',
                'at different floor'
            ]))
        self._passengers[passenger.pid] = passenger
        passenger.enter_elevator(floor)

    def leave_passenger(self, passenger, floor, time):
        if passenger.pid not in self._passengers:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'not in elevator',
                'so he/she cannot get out'
            ]))
        if self._state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot leave elevator',
                'when elevator is not serving'
            ]))
        if floor != self._floor:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot leave elevator',
                'at different floor'
            ]))
        del self._passengers[passenger.pid]

    def judge_run_speed(self, floor, time):
        if time - self._time < abs(floor - self._floor) * Elevator.run_timespan:
            raise ValueError(' '.join([
                'Elevator runs from floor',
                str(self._floor),
                'to floor',
                str(floor),
                'too fast'
            ]))
        return True

    def judge_serve_speed(self, floor, time):
        if time - self._time < Elevator.serve_timespan:
            raise ValueError(' '.join([
                'Elevator serves too fast at floor',
                str(floor)
            ]))
        return True

    def open(self, floor, time):
        if self._state == Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Elevator cannot open twice at floor',
                str(self._floor)
            ]))
        if self.judge_run_speed(floor, time):
            self._state = Elevator.State.SERVING
            self._floor = floor
            self._time = time

    def close(self, floor, time):
        if floor != self._floor:
            raise ValueError(' '.join([
                'Elevator cannot open and close at different floors'
            ]))
        if self._state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Elevator cannot close twice at floor',
                str(self._floor)
            ]))
        if self.judge_serve_speed(floor, time):
            self._state = Elevator.State.RUNNING
            self._time = time

    def serving(self):
        return self._state == Elevator.State.SERVING
