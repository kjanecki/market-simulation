import random
from multiprocessing.pool import ThreadPool

from mesa import Agent

from agents.pathfinding import compute_astar_shortest_path


class Customer(Agent):

    def __init__(self, unique_id, model, articles, shopping_list_generator):
        super().__init__(unique_id, model)
        self.articles = articles
        self.x = model.grid.width//2 + 1
        self.y = 0
        self.step_queue = []
        self.is_waiting = False
        self.is_checked = False
        self.pos = (self.x, self.y)
        self.result_async = None
        self.is_waiting_for_path = False
        self.shopping_list_generator = shopping_list_generator
        self.shopping_list = []
        self.generate_shopping_list()
        self.next_product = None
        self.in_cart_products = []
        self.steps_to_wait = 0
        self.color = "red"

    def step(self):
        if self.is_checked:
            return
        if self.is_waiting_for_path:
            if self.result_async.ready():
                self.step_queue = self.result_async.get()
                self.is_waiting_for_path = False
            return

        if len(self.step_queue) != 0:
            if self.steps_to_wait > 0:
                self.steps_to_wait -= 1
            else:
                self.move()
        elif len(self.shopping_list) > 0:
            if self.next_product is not None:
                self.in_cart_products.append(self.next_product)

            self.next_product = self.shopping_list.pop(0)
            next_product_position = self.find_product_position(self.next_product)
            self.find_path_async(next_product_position)

            self.steps_to_wait = random.randint(3, 10)

        elif self.is_waiting:
            return
        else:
            self.attempt_to_buy_products()

    def find_product_position(self, product):
        return self.model.market.get_product_position(product)

    def find_path_async(self, next_product_position):
        pass

    def find_path(self, next_product_position):
        pass

    def generate_shopping_list(self):
        pass

    def move(self):
        pass

    def attempt_to_buy_products(self):
        pass

    def check_up_products(self, n):
        products_value = 0.0
        for i in range(n):
            if len(self.in_cart_products) != 0:
                products_value += self.in_cart_products.pop(0).price

        if len(self.in_cart_products) == 0:
            self.finish_shopping()
        return products_value

    def step_forward(self):
        self.pos = (self.x, self.y)
        self.x = self.x + 1
        self.model.move_agent(self, (self.x, self.y))

    def finish_shopping(self):
        if not self.is_checked:
            self.model.remove_agent(self)
            self.is_checked = True
