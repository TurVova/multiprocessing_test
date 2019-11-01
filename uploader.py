import os
import time
import random
import queue as qq
from multiprocessing import Process, Queue

class Progress:
    _total = 0
    _done = 0
    _error = 0

    @property
    def total(self):
        return self._total

    @property
    def done(self):
        return self._done

    @property
    def error(self):
        return self._error


class Uploader:
    PATH = os.path.dirname(os.path.abspath(__file__)) + '/newfiles'

    def __init__(self, files_list, num_of_processes, queue):
        self.files_list = files_list
        self.num_of_processes = num_of_processes
        self.queue = queue
        self.performance_tasks = Queue()
        self.completed_tasks = Queue()
        self.tasks_with_errors = Queue()
        self.processes = []
        self.progress = Progress()
        self.progress._total = len(files_list)

    def uploader(self, queue):
        while True:
            try:
                task = queue.get_nowait()
                filename = task.split("/")[-1]
                os.rename(task, f'{self.PATH}/{filename}')
                self.completed_tasks.put_nowait(filename)
                time.sleep(random.randrange(start=0, stop=5)) # Simulation of a process.
            except qq.Empty:
                break
            except:
                self.tasks_with_errors.put_nowait(filename)

    def start(self):
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)

        [self.performance_tasks.put(file) for file in self.files_list]

        for _ in range(self.num_of_processes):
            process = Process(target=self.uploader, args=(self.performance_tasks,))
            process.start()
            self.processes.append(process)

    def report(self, queue):
        files = []
        if queue.qsize():
            while queue.qsize():
                file = queue.get_nowait()
                files.append(file)
            return ', '.join(files)
        else:
            return 'Nothing to show'

    def is_active(self):
        self.progress._done = self.completed_tasks.qsize()
        self.progress._error = self.tasks_with_errors.qsize()
        self.queue.put(self.progress)
        for process in self.processes:
            process.join(timeout=0)
            if process.is_alive():
                time.sleep(.1)
                os.system('clear')
                return True
        else:
            print('Done: ' + self.report(self.completed_tasks))
            print('With errors: ' + self.report(self.tasks_with_errors))
