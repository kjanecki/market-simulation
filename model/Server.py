import random

from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from Data.DataManager import DataManager
from Market.Shelf import Shelf
from agents.Checkout import Checkout
from agents.ShelfAgent import ShelfAgent
from model.MarketModel import MarketModel

article_dictionary = {}

width = 50
height = 50

regals = {}
regal_no = 0

for j in range(8, 50, 6):
    for i in range(5, 20):
        regals[str(regal_no)] = Shelf(regal_no, (i, j))
        regal_no += 1
        regals[str(regal_no)] = Shelf(regal_no, (i, j - 1))
        regal_no += 1

    for i in range(30, 45):
        regals[str(regal_no)] = Shelf(regal_no, (i, j))
        regal_no += 1
        regals[str(regal_no)] = Shelf(regal_no, (i, j - 1))
        regal_no += 1

for i in range(100):
    article_dictionary[str(i)] = random.randint(0, regal_no - 1)

checkouts = []
for i in range(4, 48, 3):
    checkouts.append((width - 1, i))

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
                     "Color": "red",
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


server = ModularServer(MarketModel,
                       [grid, queue_length_chart],
                       "Money Model",
                       {"max_agents_number": 250,
                        "width": width,
                        "height": height,
                        "market": market,
                        "checkout_slider": n_slider})
