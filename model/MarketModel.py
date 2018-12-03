# model2.py

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from agents.CommonCustomer import CommonCustomer
from Shop.Regal import Regal
from agents.RegalAgent import RegalAgent


class MarketModel(Model):

    def __init__(self, agents_number, shop, width=50, height=50):
        self.running = True
        self.shop = shop
        self.num_agents = agents_number
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.regal_agents = []

        self.place_regals()

        for i in range(self.num_agents + len(self.regal_agents)):
            a = CommonCustomer(i, self, self.shop.articles)
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))

    def place_regals(self):
        for i in range(len(self.shop.regals.keys())):
            shelf_agent = RegalAgent(i, self, list(self.shop.regals.values())[i])
            self.grid.place_agent(shelf_agent, shelf_agent.get_location())

    def step(self):
        self.schedule.step()


