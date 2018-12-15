import random

from agents.Customer import Customer
from agents.pathfinding import compute_astar_shortest_path


class CommonCustomer(Customer):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model, articles)
        self.next_article = ()
        self.is_near_checkouts = False
        self.checkout_agent = None

    def find_path(self):
        next_article_location = self.model.shop.regals[str(self.articles[str(self.shopping_list.pop(0))])].location

        i = 1
        if next_article_location[1] % 2 != 0:
            i = -1

        target_point = (next_article_location[0], next_article_location[1] + i)
        self.step_queue = compute_astar_shortest_path(self.model.space_graph, (self.x, self.y), target_point)

    def compute_rectlinear_path(self, p1, p2):
        x, y = p1[0], p1[1]

        i = 1
        if y > p2[1]:
            i = -1
        while y != p2[1]:
            y += i
            self.step_queue.append((x, y))

        i = 1
        if x > p2[0]:
            i = -1
        while x != p2[0]:
            x += i
            self.step_queue.append((x, y))

    def move(self):
        next_step = self.step_queue.pop(0)
        self.x, self.y = next_step[0], next_step[1]
        self.model.grid.move_agent(self, (self.x, self.y))

    def attempt_to_buy_products(self):
        if not self.is_near_checkouts:
            self.compute_rectlinear_path((self.x, self.y), (self.model.grid.width-3, self.y))
            self.is_near_checkouts = True
        elif self.checkout_agent is None:
            self.checkout_agent = self.model.find_nearest_checkout((self.x, self.y))
            self.compute_rectlinear_path((self.x, self.y), (self.x, self.checkout_agent.location[1]))
        else:
            pos = self.checkout_agent.stand_in_the_queue(self)
            self.compute_rectlinear_path((self.x, self.y), pos)
            self.is_waiting = True
