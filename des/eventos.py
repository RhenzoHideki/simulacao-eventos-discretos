from des.core import Event

class Arrival(Event):
    def __init__(self, time, queue, arrival_rate=0, externo=False):
        super().__init__(time)
        self.queue = queue
        self.arrival_rate = arrival_rate
        self.externo = externo

    def processing_event(self, simulator):
        queue = self.queue
        queue.arrivals += 1

        if not queue.busy:
            queue.busy = True
            queue.last_event_time = simulator.current_time
            service_time = simulator.prng.expovariate(queue.mu)
            simulator.schedule(Departure(simulator.current_time + service_time, queue))
        else:
            queue.losses += 1

        if self.externo and self.arrival_rate > 0:
            next_time = simulator.current_time + simulator.prng.expovariate(self.arrival_rate)
            simulator.schedule(Arrival(next_time, queue, self.arrival_rate, externo=True))

class Departure(Event):
    def __init__(self, time, queue):
        super().__init__(time)
        self.queue = queue

    def processing_event(self, simulator):
        queue = self.queue
        queue.completed += 1
        queue.total_busy_time += simulator.current_time - queue.last_event_time
        queue.busy = False
        queue.total_response_time += simulator.current_time - queue.last_event_time

        # Guarda o tempo da saída
        queue.departure_times.append(simulator.current_time)

        # Roteamento
        if queue.name == 'Q1':
            if simulator.prng.random() < 0.7:
                simulator.schedule(Arrival(simulator.current_time, simulator.queues['Q2']))
        elif queue.name == 'Q2':
            if simulator.prng.random() < 0.6:
                simulator.schedule(Arrival(simulator.current_time, simulator.queues['Q3']))
            else:
                simulator.schedule(Arrival(simulator.current_time, simulator.queues['Q4']))
        # Q3 e Q4 são saídas
