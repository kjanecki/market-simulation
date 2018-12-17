# model2.py
import random
from multiprocessing import Lock

import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from agents.Checkout import Checkout
from agents.CommonCustomer import CommonCustomer
from agents.ShelfAgent import ShelfAgent


class MarketModel(Model):

    def __init__(self, max_agents_number, market, width=50, height=50):
        self.running = True
        self.market = market
        self.num_agents = max_agents_number
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.grid_mutex = Lock()
        self.agents_number = 1
        self.regal_agents = []
        self.checkout_agents = []
        self.opened_checkouts = []
        self.space_graph = np.zeros((width, height))
        self.place_checkouts()
        self.place_regals()

        for i in range(3, 12, 4):
            self.open_checkout(i)
            self.opened_checkouts.append(self.checkout_agents[i])

    def add_agent(self):
        a = CommonCustomer(self.agents_number, self, self.market.articles)
        self.agents_number += 1
        self.schedule.add(a)
        self.grid.place_agent(a, (a.x, a.y))

    def place_checkouts(self):
        for checkout_location in self.market.cashRegisters:
            checkout_agent = Checkout(self.agents_number, self, checkout_location)
            self.agents_number += 1
            self.grid.place_agent(checkout_agent, checkout_location)
            self.checkout_agents.append(checkout_agent)

    def place_regals(self):
        for regal in self.market.regals:
            self.place_regal(regal)

    def place_regal(self, regal):
        for shelf in regal.shelf_list:
            self.place_shelf(shelf)

    def place_shelf(self, shelf):
        shelf_agent = ShelfAgent(self.agents_number, self, shelf)
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

    def find_nearest_checkouts(self, location, n):
        new_list = self.opened_checkouts.copy()
        ordered_list = sorted(new_list, key=(lambda x:
                                             ((x.location[0] - location[0]) ** 2) +
                                             ((x.location[1] - location[1]) ** 2)))
        return ordered_list[0:]

    def step(self):

        if len(self.schedule.agents) < self.num_agents:
            for i in range(random.randint(0, 3)):
                self.add_agent()

        self.schedule.step()

    def move_agent(self, agent, new_pos):
        # self.grid_mutex.acquire()
        self.grid.move_agent(agent, new_pos)
        # self.grid_mutex.release()

    def remove_agent(self, agent):
        # self.grid_mutex.acquire()
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)
        # self.grid_mutex.release()



