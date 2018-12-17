import random
from multiprocessing.pool import ThreadPool

from mesa import Agent

from agents.pathfinding import compute_astar_shortest_path


class Customer(Agent):

    def __init__(self, unique_id, model, articles, shopping_list_generator):
        super().__init__(unique_id, model)
        self.articles = articles
        self.products_number = random.randint(1, 3)
        self.x = model.grid.width//2 + 1
        self.y = 0
        self.step_queue = []
        self.is_waiting = False
        self.is_checked = False
        self.pos = (self.x, self.y)
        self.thread_pool = ThreadPool(1)  # TODO: Inject thread pool from model
        self.result_async = None
        self.is_waiting_for_path = False
        self.shopping_list = shopping_list_generator.generate_shopping_list(self.model.market.articles)

    def step(self):
        if self.is_checked:
            return
        if self.is_waiting_for_path:
            if self.result_async.ready():
                self.step_queue = self.result_async.get()
                self.is_waiting_for_path = False
            else:
                return

        if len(self.step_queue) != 0:
            self.move()
        elif len(self.shopping_list) > 0:
                next_product_position = self.find_product_position(self.shopping_list.pop(0))
                self.find_path_async(next_product_position)
                self.products_number += 1

        elif self.is_waiting and self.model.grid.width > self.x+1:
            if self.model.grid.is_cell_empty((self.x+1, self.y)):
                self.step_forward()
        else:
            self.attempt_to_buy_products()

    def find_product_position(self, product):
        return self.model.market.get_product_position(product)

    def find_path_async(self, next_product_position):
        pass

    def find_path(self, next_product_position):
        pass

    def move(self):
        pass

    def attempt_to_buy_products(self):
        pass

    def check_up_products(self, n):
        self.products_number -= n
        if self.products_number <= 0:
            self.finish_shopping()

    def step_forward(self):
        p = (self.x+1, self.y)
        self.model.grid.move_agent(self, p)

    def finish_shopping(self):
        self.pos = (self.x, self.y)
        if not self.is_checked:
            # self.model.grid[self.x][self.y].remove(self)
            self.is_checked = True
