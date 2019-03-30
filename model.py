from enum import Enum, unique


class Passenger:
    def __init__(self, pid, start, target):
        self.__pid = pid
        self.__floor = start
        self.__target = target
        self.__in_elevator = False

    @property
    def pid(self):
        return self.__pid

    @property
    def floor(self):
        return self.__floor

    @property
    def target(self):
        return self.__target

    @property
    def in_elevator(self):
        return self.__in_elevator

    def enter_elevator(self, enter_floor):
        if self.__in_elevator:
            raise ValueError(' '.join([
                'Passenger',
                str(self.__pid),
                'cannot enter the elevator twice at floor',
                str(enter_floor)
            ]))
        if self.__floor != enter_floor:
            raise ValueError(' '.join([
                'Passenger',
                str(self.__pid),
                'cannot enter the elevator',
                'at another floor'
            ]))
        self.__floor = enter_floor
        self.__in_elevator = True

    def leave_elevator(self, leave_floor):
        if not self.__in_elevator:
            raise ValueError(' '.join([
                'Passenger',
                str(self.__pid),
                'cannot leave the elevator twice at floor',
                str(leave_floor)
            ]))
        self.__floor = leave_floor
        self.__in_elevator = False


class Elevator:
    run_timespan = 0.5
    serve_timespan = 0.5

    @unique
    class State(Enum):
        STOPPED = 0,
        RUNNING = 1,
        SERVING = 2

    def __init__(self):
        self.__floor = 1
        self.__time = 0.0
        self.__state = Elevator.State.STOPPED
        self.__passengers = {}

    @property
    def floor(self):
        return self.__floor

    @property
    def time(self):
        return self.__time

    @property
    def state(self):
        return self.__state

    def enter_passenger(self, passenger, floor, time):
        if passenger.pid in self.__passengers:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'already in the elevator',
                'so he/she cannot get in'
            ]))
        if self.__state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot enter the elevator',
                'when the elevator is not serving'
            ]))
        if floor != self.__floor:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot enter the elevator',
                'at a different floor floor'
            ]))
        passenger.enter_elevator(floor)
        self.__passengers[passenger.pid] = passenger

    def leave_passenger(self, passenger, floor, time):
        if passenger.pid not in self.__passengers:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'not in the elevator',
                'so he/she cannot get out'
            ]))
        if self.__state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot leave the elevator',
                'when the elevator is not serving'
            ]))
        if floor != self.__floor:
            raise ValueError(' '.join([
                'Passenger',
                str(passenger.pid),
                'cannot leave the elevator',
                'at a different floor floor'
            ]))
        passenger.leave_elevator(floor)
        del self.__passengers[passenger.pid]

    def judge_run_speed(self, floor, time):
        if time - self.__time < abs(floor - self.__floor) * Elevator.run_timespan:
            raise ValueError(' '.join([
                'Elevator runs from floor',
                str(self.__floor),
                'to floor',
                str(floor),
                'too fast'
            ]))
        return True

    def judge_serve_speed(self, floor, time):
        if time - self.__time < Elevator.serve_timespan:
            raise ValueError(' '.join([
                'Elevator serves too fast at floor',
                str(floor)
            ]))
        return True

    def open(self, floor, time):
        if self.__state == Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Elevator cannot open twice at floor',
                str(self.__floor)
            ]))
        if self.judge_run_speed(floor, time):
            self.__state = Elevator.State.SERVING
            self.__floor = floor
            self.__time = time

    def close(self, floor, time):
        if floor != self.__floor:
            raise ValueError(' '.join([
                'Elevator cannot open and close at different floors'
            ]))
        if self.__state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Elevator cannot close twice at floor',
                str(self.__floor)
            ]))
        if self.judge_serve_speed(floor, time):
            self.__state = Elevator.State.RUNNING
            self.__time = time

    def serving(self):
        return self.__state == Elevator.State.SERVING
