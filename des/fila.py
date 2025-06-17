class QueueServer:
    def __init__(self, name, mu):
        self.name = name
        self.mu = mu
        self.busy = False
        self.arrivals = 0
        self.losses = 0
        self.total_busy_time = 0
        self.last_event_time = 0
        self.completed = 0
        self.total_response_time = 0
