import random

from mesa import Agent


class Checkout(Agent):

    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.is_opened = False
        self.queue = []
        self.is_processing = False
        self.location = location
        self.served_agent = None

    def step(self):
        if self.is_opened:
            self.serve_customer()

    def serve_customer(self):
        if self.is_processing:
            self.served_agent.check_up_products(random.randint(1, 3))
            if self.served_agent.is_checked_up():
                self.is_processing = False
        else:
            self.start_serving()


    def start_serving(self):
        if len(self.queue) > 0:
            self.is_processing = True
            self.served_agent = self.queue.pop(0)
            self.serve_customer()

    def close(self):
        self.is_opened = False

    def open(self):
        self.is_opened = True

    def stand_int_the_queue(self, agent):
        self.queue.append(agent)



