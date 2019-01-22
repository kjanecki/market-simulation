import random

import numpy as np
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from Data.DataManager import DataManager
from Market.Shelf import Shelf
from agents.Checkout import Checkout
from agents.ShelfAgent import ShelfAgent
from model.MarketModel import MarketModel

from model.handlers import CustomersHandler, ColorChangeHandler, AgentCountsHandler

article_dictionary = {}

width = 50
height = 50

market = DataManager.initialize_market()


def agent_portrayal(agent):
    if type(agent) is ShelfAgent:
        portrayal = {"Shape": "rect",
                     "Color": "blue",
                     "Filled": "true",
                     "Layer": 0,
                     "w": 0.9,
                     "h": 0.9}

    elif type(agent) is Checkout:
        portrayal = {"Shape": "rect",
                     "Color": "black",
                     "Filled": "true",
                     "Layer": 0,
                     "w": 0.9,
                     "h": 0.9}
        if agent.is_opened:
            portrayal["Color"] = "green"
    else:
        portrayal = {"Shape": "circle",
                     "Color": agent.color,
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.5}

        if agent.is_checked:
            portrayal["Color"] = "white"
    return portrayal


chart = ChartModule([{"Label": "total_income",
                      "Color": "Black"}],
                    data_collector_name='income_data_collector')

queue_length_chart = ChartModule([{"Label": "average_queue_length",
                                   "Color": "Blue"}],
                                 data_collector_name='queue_length_data_collector')

grid = CanvasGrid(agent_portrayal, width, height, width * 10, height * 10)


n_slider = UserSettableParameter('slider', "Number of opened checkouts", 3, 1, len(market.cashRegisters)-1, 1)


buff = []
plot_buff = []
customers_handler = ("/users?", CustomersHandler, {"market_buff": buff})
customer_color_handler = ("/color?", ColorChangeHandler, {"market_buff": buff})
agent_counts_handler = ("/agent_counts?", AgentCountsHandler, {"market_buff": plot_buff})


class MyServer(ModularServer):

    def __init__(self, buf, plot_buff, model_cls, visualization_elements, name="Mesa Model", model_params={}):
        self.handlers.append(customers_handler)
        self.handlers.append(customer_color_handler)
        self.handlers.append(agent_counts_handler)
        super().__init__(model_cls, visualization_elements, name, model_params)
        self.buffer = buf
        self.plot_buff = plot_buff


server = MyServer(buff, plot_buff, MarketModel,
                       [grid, queue_length_chart],
                       "Money Model",
                       {"buff": buff,
                        "plot_buff": plot_buff,
                        "max_agents_number": 250,
                        "width": width,
                        "height": height,
                        "market": market,
                        "checkout_slider": n_slider})