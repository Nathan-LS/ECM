from service.service_module import *
from threading import Lock
from PyQt5.QtCore import *
import time
import datetime


class task_object(QRunnable):
    def __init__(self, function_ptr, interval_=60, run_immediately=True, pass_time=False):
        super(task_object, self).__init__()
        assert isinstance(interval_, int)
        assert isinstance(run_immediately, bool)
        self.__interval = interval_
        self.__function = function_ptr
        self.__next_run = datetime.datetime.utcnow() if run_immediately else datetime.datetime.utcnow() + datetime.timedelta(
            seconds=self.__interval)
        self.__last_run = datetime.datetime.utcnow()
        self.__container_time = datetime.datetime.utcnow()
        self.__pass_time_to_function = pass_time
        self.setAutoDelete(False)

    def __lt__(self, other):
        return self.next_run < other.next_run

    def __gt__(self, other):
        return self.next_run > other.next_run

    @property
    def next_run(self):
        return self.__next_run

    @property
    def function(self):
        return self.__function

    def set_time_now(self, time_now):
        assert isinstance(time_now, datetime.datetime)
        self.__container_time = time_now

    def run(self):
        if self.__ready_to_run():
            try:
                if self.__pass_time_to_function:
                    self.__function(self.__container_time)
                    self.__update_next_run()
                else:
                    self.__function()
                    self.__update_next_run()
            except Exception as ex:
                print(ex)

    def __update_next_run(self):
        self.__next_run = self.__container_time + datetime.timedelta(seconds=self.__interval)
        self.__last_run = self.__container_time

    def change_interval(self, seconds):
        self.__interval = seconds
        self.__update_next_run()

    def force_run_now(self):
        self.__next_run = datetime.datetime.utcnow()

    def run_once_in_seconds(self, seconds):
        try:
            self.__next_run = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        except Exception as ex:
            print(ex)

    def __ready_to_run(self):
        if self.__container_time >= self.__next_run:
            return True
        else:
            return False


class task_container(QObject):
    signal_tasks_starting = pyqtSignal()
    signal_tasks_finished = pyqtSignal()
    signal_tasks_count_completed = pyqtSignal(int)

    def __init__(self, thread_count: int, auto_sort=True, pass_time=False):
        super(task_container, self).__init__()
        self.__tasks = []
        self.__lock = Lock()
        self.__auto_sort = auto_sort
        self.__pool = QThreadPool()
        self.__pool.setMaxThreadCount(thread_count)
        self.__pass_time = pass_time

    def __get_task(self, function_ptr):
        for i in self.__tasks:
            assert isinstance(i, task_object)
            if function_ptr == i.function:
                return i
        return None

    def __get_task_index(self, function_ptr):
        index = 0
        for i in self.__tasks:
            if function_ptr == i.function:
                return index
            index += 1
        return None

    def __sort_tasks(self):
        if self.__auto_sort:
            self.__tasks.sort()

    def add_task(self, function_ptr, seconds_interval, run_now=False):
        """adds a tasks given a function pointer and a second interval"""
        with self.__lock:
            task_ = self.__get_task(function_ptr)
            if task_:
                task_.change_interval(seconds_interval)
                if run_now:
                    task_.force_run_now()
                self.__sort_tasks()
            else:
                self.__tasks.append(task_object(function_ptr, seconds_interval, run_now, pass_time=self.__pass_time))

    def force_task(self, function_ptr):
        task_ = self.__get_task(function_ptr)
        if task_:
            task_.force_run_now()
            self.__sort_tasks()

    def remove_task(self, function_ptr):
        """remove a tasks with a given function pointer"""
        with self.__lock:
            index = self.__get_task_index(function_ptr)
            if index is not None:
                self.__tasks.pop(index)
                self.__sort_tasks()

    def retry_task(self, function_ptr, seconds_run):
        task_ = self.__get_task(function_ptr)
        if task_:
            task_.run_once_in_seconds(seconds=seconds_run)

    def clear_tasks(self):
        """removes all tasks"""
        with self.__lock:
            self.__tasks.clear()

    def run_tasks(self, ):
        """run all runnable tasks"""
        # self.signal_tasks_starting.emit()
        time_now = datetime.datetime.utcnow()
        for i in self.__tasks:
            assert isinstance(i, task_object)
            i.set_time_now(time_now)
            self.__pool.start(i)
        self.__pool.waitForDone()
        self.__sort_tasks()
        # self.signal_tasks_finished.emit()
        # self.signal_tasks_count_completed.emit(total_tasks)

    @property
    def next_task(self):
        """returns a datetime of the next task to run, else returns none if empty or list is not autosorted"""
        try:
            if self.__auto_sort:
                return self.__tasks[0].next_run
            else:
                return None
        except:
            return None


class task_runner(QThread):
    def __init__(self, task_container_, run_interval_seconds: int = 1):
        super(task_runner, self).__init__()
        self.__tasks = task_container_
        self.__run_task = True
        self.__interval = run_interval_seconds
        assert isinstance(self.__tasks, task_container)
        assert isinstance(self.__interval, int)

    def run(self):
        while self.__run_task:
            self.__tasks.run_tasks()
            time.sleep(self.__interval)


class Scheduler_service(QObject):
    def __init__(self):
        super(Scheduler_service, self).__init__()

        self.tasks_time = task_container(thread_count=1, auto_sort=False, pass_time=True)
        self.tasks_api = task_container(thread_count=4, auto_sort=True)

        self.__master_tasks = task_container(thread_count=2, auto_sort=False)
        self.__master_thread = task_runner(task_container_=self.__master_tasks, run_interval_seconds=1)
        self.__master_thread.start()

        self.__master_tasks.add_task(self.tasks_time.run_tasks, seconds_interval=1, run_now=True)
        self.__master_tasks.add_task(self.tasks_api.run_tasks, seconds_interval=5, run_now=True)
