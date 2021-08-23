import time
from typing import *

class EventData:
    def __init__(self, domain_name, times):
        """
           domain_name: Domain name
           times: List of times in mileseconds to track [600000, 60000] - 10 minutes and 1 minute
        """
        self.data = {}
        for rec_time in times:
            self.data[rec_time] = {
                'counter_data': [],
                'counter': 0,
            }
        self.domain_name = domain_name
    
    def add_event(self, event):
        if self.domain_name in event:
            count = event[self.domain_name]
            for counter_entry in self.data.values():
                counter_entry['counter_data'].append(event)
                counter_entry['counter'] += count

        self.remove_old()

    def remove_old(self, cur_time = None):
        self.__remove_old(cur_time)
    
    def value(self, period:int , update_time = None):
        if update_time is None:
            update_time = time.time() * 1000

        if self.update_time != update_time:
            self.__remove_old()

        return self.data[period]['counter']

    def __remove_old(self, curtime = None):
        if curtime is None:
            curtime = time.time() * 1000 # to unix time
        self.update_time = curtime

        # update enties
        for entry_time, counter_entry in self.data.items():
            updated_list, count_to_remove = self.__remove_from_list(curtime,
                                                                counter_entry['counter_data'],
                                                                entry_time)
            counter_entry['counter_data'] = updated_list
            counter_entry['counter'] -= count_to_remove
    
    def __remove_from_list(self, curtime, data_list, time_period):
        # remove old event count and cut the list for given time period
        counter = 0
        events_count_to_remove = 0
        for event in data_list:
            if curtime - event['timestamp'] > time_period:
                counter += 1
                events_count_to_remove += event[self.domain_name]
            else:
                break
        return data_list[counter:], events_count_to_remove