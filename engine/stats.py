import time
from engine.event_data import EventData
import threading
from typing import *
import queue
from django.conf import settings


class DataThread(threading.Thread):
    """
        This class updates and saves data 
    """
    _instance = None
    _kueue = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            with cls._lock:
                if not isinstance(cls._instance, cls):
                    cls._instance = object.__new__(cls, *args, **kwargs)
                    cls._instance.init()
        return cls._instance

    def init(self):
        super(DataThread, self).__init__()
        self.all = {}
        self.daemon = True
        self._kueue = queue.Queue()
        self.start()

    def add_events(self, events):
        self._kueue.put(events)

    def run(self):
        while True:
            self._do_update()

    def _do_update(self):
        kueue = self._kueue
        row = kueue.get(block=True)
        self.__update_data(row)
        while not kueue.empty():
            row = kueue.get()
            self.__update_data(row)
    
    def get_maxes(self, period, enties):
        cur_time = time.time() * 1000
        for item in self.all.values():
            item.remove_old(cur_time)
        items = sorted(self.all.values(), key=lambda x: x.value(period, cur_time), reverse=True)[0: enties]
        return {item.domain_name: item.value(period, cur_time) for item in items}

    def __update_data(self, row:Dict):
        for key in row.keys():
            if key != 'timestamp':
                if key not in self.all:
                    self.all[key] = EventData(key, settings.TIMES)
                with DataThread._lock:
                    self.all[key].add_event(row)
