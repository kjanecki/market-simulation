# model2.py
import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from agents.Checkout import Checkout
from agents.CommonCustomer import CommonCustomer
from agents.RegalAgent import RegalAgent


class MarketModel(Model):

    def __init__(self, agents_number, shop, width=50, height=50):
        self.running = True
        self.shop = shop
        self.num_agents = agents_number
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.agents_number = 1
        self.regal_agents = []
        self.checkout_agents = []
        self.opened_checkouts = []
        self.space_graph = np.zeros((width, height))

        self.place_checkouts()
        self.place_regals()

        self.agents_number += 1
        for i in range(self.num_agents):
            a = CommonCustomer(self.agents_number, self, self.shop.articles)
            self.agents_number += 1
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))

        for i in range(1, 4, 2):
            self.open_checkout(i)
            self.opened_checkouts.append(self.checkout_agents[i])

    def place_checkouts(self):
        for checkout_location in self.shop.cashRegisters:
            checkout_agent = Checkout(self.agents_number, self, checkout_location)
            self.agents_number += 1
            self.grid.place_agent(checkout_agent, checkout_location)
            self.checkout_agents.append(checkout_agent)

    def place_regals(self):
        for i in range(len(self.shop.regals.keys())):
            shelf_agent = RegalAgent(self.agents_number, self, list(self.shop.regals.values())[i])
            pos = shelf_agent.get_location()
            self.agents_number += 1
            self.grid.place_agent(shelf_agent, pos)
            self.regal_agents.append(shelf_agent)
            self.space_graph[pos[0], pos[1]] = 1

    def open_checkout(self, n):
        if n > len(self.checkout_agents):
            return
        else:
            self.checkout_agents[n].open()
            self.schedule.add(self.checkout_agents[n])

    def find_nearest_checkout(self, location):

        min_checkout = self.opened_checkouts[0]
        min_height_distance = abs(location[1] - min_checkout.location[1])
        for i in self.opened_checkouts:
            height_distance = abs(location[1] - i.location[1])
            if height_distance < min_height_distance:
                min_height_distance = height_distance
                min_checkout = i

        return min_checkout

    def step(self):
        self.schedule.step()


