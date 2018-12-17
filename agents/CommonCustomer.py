import random

from Data.ShoppingListsGenerator import ShoppingListGenerator
from agents.Customer import Customer
from agents.pathfinding import compute_astar_shortest_path


class CommonCustomer(Customer):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model, articles, ShoppingListGenerator())
        self.next_article = ()
        self.is_near_checkouts = False
        self.checkout_agent = None

    def find_path(self, target_point):
        self.step_queue = compute_astar_shortest_path(self.model.space_graph, (self.x, self.y), target_point)

    def find_path_async(self, next_product_position):
        self.result_async = self.thread_pool.apply_async(compute_astar_shortest_path,
                                                         (self.model.space_graph, (self.x, self.y),
                                                          next_product_position))
        self.is_waiting_for_path = True

    def move(self):
        next_step = self.step_queue.pop(0)
        self.x, self.y = next_step[0], next_step[1]
        self.model.grid.move_agent(self, (self.x, self.y))

    def attempt_to_buy_products(self):
        if not self.is_near_checkouts:
            self.find_path((self.model.grid.width-3, self.y))
            self.is_near_checkouts = True
        elif self.checkout_agent is None:
            self.checkout_agent = self.model.find_nearest_checkout((self.x, self.y))
            self.find_path((self.x, self.checkout_agent.location[1]))
        else:
            pos = self.checkout_agent.stand_in_the_queue(self)
            self.find_path(pos)
            self.is_waiting = True
