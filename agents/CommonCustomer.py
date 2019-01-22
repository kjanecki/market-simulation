import random

from Data.ShoppingListsGenerator import ShoppingListGenerator
from agents.Customer import Customer
from agents.pathfinding import compute_astar_shortest_path


class CommonCustomer(Customer):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model, articles, ShoppingListGenerator(model.market))
        self.next_article = ()
        self.is_near_checkouts = False
        self.checkout_agent = None

    def find_path(self, target_point):
        h = 'distance'
        if random.randint(0, 2) == 1:
            h = 'manhattan'
        self.step_queue = compute_astar_shortest_path(self.model.space_graph, (self.x, self.y), target_point, h)

    def find_path_async(self, next_product_position):
        h = 'distance'
        if random.randint(0, 1) == 1:
            h = 'manhattan'

        self.result_async = self.model.thread_pool.apply_async(compute_astar_shortest_path,
                                                         (self.model.space_graph, (self.x, self.y),
                                                          next_product_position,
                                                          h))
        self.is_waiting_for_path = True

    def move(self):
        next_step = self.step_queue.pop(0)
        self.pos = (self.x, self.y)
        self.x, self.y = next_step[0], next_step[1]
        self.model.move_agent(self, (self.x, self.y))

    def attempt_to_buy_products(self):
        if not self.is_near_checkouts:
            self.find_path((self.model.grid.width-3, self.y))
            self.is_near_checkouts = True
        elif self.checkout_agent is None:
            self.choose_checkout(self.model.find_nearest_checkouts((self.x, self.y), 3), 3)
            self.find_path((self.x, self.checkout_agent.location[1]))
        else:
            pos = self.checkout_agent.stand_in_the_queue(self)
            self.find_path(pos)
            self.is_waiting = True

    def choose_checkout(self, checkouts, threshold):
        chosen_checkout = checkouts[0]
        for checkout in checkouts[1:len(checkouts)]:
            if len(checkout.queue) + threshold < len(chosen_checkout.queue):
                chosen_checkout = checkout

        self.checkout_agent = chosen_checkout

    def generate_shopping_list(self):
        self.shopping_list = self.shopping_list_generator.generate_shopping_list(self.model.market.articles, True)


class LazyCustomer(CommonCustomer):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model, articles)
        self.delay = 1

    def generate_shopping_list(self):
        self.shopping_list = self.shopping_list_generator.generate_shopping_list(self.model.market.articles, False)

    def move(self):
        self.delay = (self.delay + 1) % 2
        if self.delay == 0:
            super().move()

