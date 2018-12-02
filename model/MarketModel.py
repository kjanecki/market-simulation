# model2.py
import random

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from model.CommonCustomer import CommonCustomer


class MarketModel(Model):

    def __init__(self, agents_number, articles, width=50, height=50):
        self.running = True
        self.articles = articles
        self.num_agents = agents_number
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)

        for i in range(self.num_agents):
            a = CommonCustomer(i, self, articles)
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))

    def step(self):
        self.schedule.step()


