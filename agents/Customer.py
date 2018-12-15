import random

from mesa import Agent


class Customer(Agent):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model)
        self.articles = articles
        self.products_number = random.randint(1, 3)
        self.x = model.grid.width//2 + 1
        self.y = 0
        self.step_queue = []
        self.is_waiting = False
        self.is_checked = False
        self.pos = (self.x, self.y)
        self.shopping_list = generate_shopping_list(articles, self.products_number)

    def step(self):
        if self.is_checked:
            return

        if len(self.step_queue) != 0:
            self.move()
        elif len(self.shopping_list) > 0:
                self.find_path()
                self.products_number += 1
                self.move()
        elif self.is_waiting and self.model.grid.width > self.x+1:
            if self.model.grid.is_cell_empty((self.x+1, self.y)):
                self.step_forward()
        else:
            self.attempt_to_buy_products()

    def find_path(self):
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


def generate_shopping_list(articles, number):
    return random.sample(range(len(list(articles.keys()))), number)
