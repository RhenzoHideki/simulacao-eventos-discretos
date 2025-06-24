import heapq

class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

class Simulator:
    def __init__(self, end_time, prng):
        self.current_time = 0
        self.event_queue = []
        self.end_time = end_time
        self.queues = {}
        self.prng = prng

    def schedule(self, event):
        heapq.heappush(self.event_queue, event)

    def run(self):
        while self.event_queue and self.current_time < self.end_time:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            event.processing_event(self)
