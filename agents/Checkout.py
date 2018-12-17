import random
from multiprocessing import Lock

from mesa import Agent


class Checkout(Agent):

    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.is_opened = False
        self.queue = []
        self.is_serving = False
        self.location = location
        self.served_agent = None
        self.queue_mutex = Lock()
        self.queue_end_location = (location[0], location[1] - 1)

    def step(self):
        if self.is_opened:
            self.serve_customer()

    def serve_customer(self):
        if self.is_serving:
            self.served_agent.check_up_products(1)
            if self.served_agent.is_checked:
                self.push_forward_queue_end_location()
                self.is_serving = False
        else:
            self.start_serving()

    def start_serving(self):
        if len(self.queue) > 0:
            for customer in self.queue:
                customer.step_forward()

            self.is_serving = True
            self.served_agent = self.queue.pop(0)
            self.serve_customer()

    def close(self):
        self.is_opened = False

    def open(self):
        self.is_opened = True

    def stand_in_the_queue(self, agent):
        return self.enqueue(agent)

    def enqueue(self, agent):
        self.queue_mutex.acquire()
        self.queue.append(agent)
        old_queue_end_location = self.queue_end_location
        if self.queue_end_location[0] - 1 >= 0:
            self.queue_end_location = (self.queue_end_location[0] - 1, self.queue_end_location[1])
        self.queue_mutex.release()
        return old_queue_end_location

    def push_forward_queue_end_location(self):
        self.queue_mutex.acquire()
        if self.queue_end_location[0] + 1 < self.model.grid.width:
            self.queue_end_location = (self.queue_end_location[0] + 1, self.queue_end_location[1])
        self.queue_mutex.release()

    def get_queue_end_location(self):
        return self.queue_end_location



