# model2.py
import random
from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from agents.Checkout import Checkout
from agents.CommonCustomer import CommonCustomer, LazyCustomer
from agents.ShelfAgent import ShelfAgent


def get_income(model):
    return model.total_income


def compute_average_queue_size(model):
    return round(np.average([len(checkout.queue) for checkout in model.opened_checkouts]))


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def get_agent_counts(model):
    return model.agent_counts


class MarketModel(Model):

    def __init__(self, buff, plot_buff, max_agents_number, market, checkout_slider, width=50, height=50, steps=3000):
        self.steps = steps
        self.plot_buff = plot_buff
        self.running = True
        self.market = market
        self.checkout_slider = checkout_slider
        self.num_agents = max_agents_number
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.grid_mutex = Lock()
        self.agents_number = 1
        self.regal_agents = []
        self.checkout_agents = []
        self.opened_checkouts = []
        self.closed_checkouts = []
        self.space_graph = np.zeros((width, height))
        self.place_checkouts()
        self.place_regals()
        self.thread_pool = ThreadPool(20)
        self.customer_list = buff
        self.total_income = 0.0
        self.agent_counts = [[0 for x in range(self.grid.width)] for y in range(self.grid.height)]
        self.plot_buff.append(self.agent_counts)
        self.plot_buff.append(self.grid.width)
        self.plot_buff.append(self.grid.height)
        self.income_data_collector = DataCollector(
            model_reporters={"total_income": get_income})

        self.queue_length_data_collector = DataCollector(
            model_reporters={"average_queue_length": compute_average_queue_size})

        self.open_checkouts()

    def add_agent(self):
        i = random.randint(0, 1)
        if i == 0:
            a = CommonCustomer(self.agents_number, self, self.market.articles)
        else:
            a = LazyCustomer(self.agents_number, self, self.market.articles)
        # a = CommonCustomer(self.agents_number, self, self.market.articles)
        self.agents_number += 1
        self.schedule.add(a)
        self.grid.place_agent(a, (a.x, a.y))
        self.customer_list.append(a)

    def place_checkouts(self):
        for checkout_location in self.market.cashRegisters:
            checkout_agent = Checkout(self.agents_number, self, checkout_location)
            self.agents_number += 1
            self.grid.place_agent(checkout_agent, checkout_location)
            self.checkout_agents.append(checkout_agent)
        self.closed_checkouts = self.checkout_agents

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

    def open_checkouts(self):
        for i in range(0, len(self.checkout_agents), len(self.checkout_agents)//self.checkout_slider):
            checkout = self.closed_checkouts.pop(random.randint(0, len(self.closed_checkouts)-1))
            checkout.open()
            self.opened_checkouts.append(checkout)
            self.schedule.add(checkout)

    def open_random_checkout(self):
        if len(self.closed_checkouts) != 0:
            checkout = self.closed_checkouts.pop(random.randint(0, len(self.closed_checkouts) - 1))
            checkout.open()
            self.opened_checkouts.append(checkout)
            self.schedule.add(checkout)

    def close_random_checkout(self):
        if len(self.opened_checkouts) > 1:
            checkout = self.opened_checkouts.pop(random.randint(0, len(self.opened_checkouts) - 1))
            checkout.close()
            self.closed_checkouts.append(checkout)
            # self.schedule.add(checkout)

    def find_nearest_checkouts(self, location, n):
        new_list = self.opened_checkouts.copy()
        ordered_list = sorted(new_list, key=(lambda x:
                                             ((x.location[0] - location[0]) ** 2) +
                                             ((x.location[1] - location[1]) ** 2)))
        return ordered_list[0:]

    def step(self):
        print(self.checkout_slider)
        self.income_data_collector.collect(self)
        self.queue_length_data_collector.collect(self)

        if compute_average_queue_size(self) > 3:
            self.open_random_checkout()

        if compute_average_queue_size(self) < 3:
            self.close_random_checkout()

        sigma = 1
        cycle_steps = 1500
        n = self.schedule.steps // cycle_steps + 1
        gauss = gaussian(self.schedule.steps * (6 * sigma / cycle_steps) - 3 * n * sigma, 0, sigma) * self.num_agents
        print(gauss)
        while len(self.schedule.agents) - len(self.checkout_agents) < np.ceil(gauss):
            self.add_agent()

        self.schedule.step()

    def move_agent(self, agent, new_pos):
        # self.grid_mutex.acquire()
        self.agent_counts[new_pos[0]][new_pos[1]] += 1
        self.plot_buff[0] = self.agent_counts
        self.grid.move_agent(agent, new_pos)
        # self.grid_mutex.release()

    def remove_agent(self, agent):
        # self.grid_mutex.acquire()
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)
        if type(agent) is CommonCustomer:
            self.customer_list.remove(agent)
        # self.grid_mutex.release()

    def get_customers(self):
        return self.customer_list


