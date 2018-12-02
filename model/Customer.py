import random

from mesa import Agent


class Customer(Agent):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model)
        self.articles = articles
        self.shopping_list = generate_shopping_list(articles)
        self.x = 0
        self.y = 0
        self.step_queue = []

    def step(self):
        if len(self.shopping_list) > 0:

            if len(self.step_queue) == 0:
                self.find_path()
            else:

                self.move()
        else:
            self.go_to_checkout()

    def find_path(self):
        pass

    def move(self):
        pass

    def go_to_checkout(self):
        pass


def generate_shopping_list(articles):
    return random.sample(range(len(list(articles.keys()))), random.randint(5, 10))
