from enum import Enum, unique


class Passenger:
    def __init__(self, pid, start, target, time):
        self.__pid = pid
        self.__floor = start
        self.__target = target
        self.__time = time
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
    def time(self):
        return self.__time

    @property
    def in_elevator(self):
        return self.__in_elevator

    def enter_elevator(self, enter_floor):
        if self.__in_elevator:
            raise ValueError(' '.join([
                'Wrong State |',
                'Passenger',
                str(self.__pid),
                'cannot enter the elevator twice at floor',
                str(enter_floor)
            ]))
        if self.__floor != enter_floor:
            raise ValueError(' '.join([
                'Wrong State |',
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
                'Wrong State |',
                'Passenger',
                str(self.__pid),
                'cannot leave the elevator twice at floor',
                str(leave_floor)
            ]))
        self.__floor = leave_floor
        self.__in_elevator = False


class Elevator:
    run_timespan = 0.4
    serve_timespan = 0.5
    eps = 1e-8

    @unique
    class State(Enum):
        STOPPED = 0,
        RUNNING = 1,
        SERVING = 2

    def __init__(self):
        self.__floor = 1
        self.__time = 0.0
        self.__last_arrive_floor = 1
        self.__last_arrive_time = 0.0
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

    def arrive(self, floor, time):
        before_floor = self.__last_arrive_floor
        after_floor = floor
        if before_floor < 0:
            before_floor += 1
        if after_floor < 0:
            after_floor += 1
        if abs(after_floor - before_floor) != 1:
            raise ValueError(' '.join([
                'Wrong State |',
                'Elevator cannot arrive',
                'from floor',
                str(self.__last_arrive_floor),
                'to floor',
                str(floor)
            ]))
        if time - self.__last_arrive_time + Elevator.eps < Elevator.run_timespan:
            raise ValueError(' '.join([
                'Wrong State |',
                'Elevator arrives from floor',
                str(self.__last_arrive_floor),
                'to',
                str(floor),
                'too fast'
            ]))
        self.__last_arrive_floor = floor
        self.__last_arrive_time = time

    def enter_passenger(self, passenger, floor, time):
        if passenger.pid in self.__passengers:
            raise ValueError(' '.join([
                'Wrong State |',
                'Passenger',
                str(passenger.pid),
                'already in the elevator',
                'so he/she cannot get in'
            ]))
        if self.__state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Wrong State |',
                'Passenger',
                str(passenger.pid),
                'cannot enter the elevator',
                'when the elevator is not serving'
            ]))
        if floor != self.__floor:
            raise ValueError(' '.join([
                'Wrong State |',
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
                'Wrong State |',
                'Passenger',
                str(passenger.pid),
                'not in the elevator',
                'so he/she cannot get out'
            ]))
        if self.__state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Wrong State |',
                'Passenger',
                str(passenger.pid),
                'cannot leave the elevator',
                'when the elevator is not serving'
            ]))
        if floor != self.__floor:
            raise ValueError(' '.join([
                'Wrong State |',
                'Passenger',
                str(passenger.pid),
                'cannot leave the elevator',
                'at a different floor floor'
            ]))
        passenger.leave_elevator(floor)
        del self.__passengers[passenger.pid]

    def judge_run_speed(self, floor, time):
        before_floor = self.__floor
        after_floor = floor
        if before_floor < 0:
            before_floor += 1
        if after_floor < 0:
            after_floor += 1
        if time - self.__time + Elevator.eps < abs(after_floor - before_floor) * Elevator.run_timespan:
            raise ValueError(' '.join([
                'Time Error |',
                'Elevator runs from floor',
                str(self.__floor),
                'to floor',
                str(floor),
                'too fast'
            ]))
        return True

    def judge_serve_speed(self, floor, time):
        if time - self.__time + Elevator.eps < Elevator.serve_timespan:
            raise ValueError(' '.join([
                'Time Error |',
                'Elevator serves too fast at floor',
                str(floor)
            ]))
        return True

    def open(self, floor, time):
        if self.__state == Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Wrong State |',
                'Elevator cannot open twice at floor',
                str(self.__floor)
            ]))
        if floor != self.__last_arrive_floor:
            raise ValueError(' '.join([
                'Wrong State |',
                'Elevator cannot open at floor',
                str(floor),
                'before it arrives'
            ]))
        if self.judge_run_speed(floor, time):
            self.__state = Elevator.State.SERVING
            self.__floor = floor
            self.__time = time

    def close(self, floor, time):
        if floor != self.__floor:
            raise ValueError(' '.join([
                'Wrong State |',
                'Elevator cannot open and close at different floors'
            ]))
        if self.__state != Elevator.State.SERVING:
            raise ValueError(' '.join([
                'Wrong State |',
                'Elevator cannot close twice at floor',
                str(self.__floor)
            ]))
        if self.judge_serve_speed(floor, time):
            self.__state = Elevator.State.RUNNING
            self.__time = time

    def serving(self):
        return self.__state == Elevator.State.SERVING
