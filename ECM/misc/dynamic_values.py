import datetime


class dynamic_values(object):
    start_time = None
    end_time = None

    def __init__(self, start_time=datetime.datetime.utcnow(), end_time=datetime.datetime.utcnow()):
        self.start_time = start_time
        self.end_time = end_time

    def time_difference(self, time_now=datetime.datetime.utcnow()) -> datetime:
        try:
            __time_delta = self.start_time - time_now
            if __time_delta.days >= 0:
                return __time_delta
            else:
                return None
        except Exception as ex:
            return None

    def __str__(self):
        return ""


class dynamic_sp_counter(dynamic_values):
    def __init__(self, start_time=datetime.datetime.utcnow(), starting_sp: int = 0, sp_hr: int = 0):
        super(dynamic_sp_counter, self).__init__(start_time + datetime.timedelta(minutes=60), start_time)
        self.__starting_sp = starting_sp
        self.__sp_hr = sp_hr

    def __str__(self):
        td = self.time_difference(self.end_time)
        if td is None or self.__starting_sp is None:
            return "0"
        else:
            __total_sp = self.__starting_sp + (self.__sp_hr - (self.__sp_hr * (td.seconds / 3600)))
            return "{:,}".format(int(__total_sp))

    def update_time(self, time):
        self.end_time = time
        return self.__str__()


class dynamic_countdown(dynamic_values):
    def __init__(self, runs_at=datetime.datetime.utcnow(), time_now=datetime.datetime.utcnow()):
        super(dynamic_countdown, self).__init__(runs_at, time_now)

    def __str__(self):
        td = self.time_difference(self.end_time)
        if td is None:
            return ""
        else:
            return "{:02d}:{:02d}".format(int(td.seconds / 60), int(td.seconds % 60))
