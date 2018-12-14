import random

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Shop.Shop import Shop
from Shop.Regal import Regal
from agents.Checkout import Checkout
from agents.RegalAgent import RegalAgent
from model.MarketModel import MarketModel

article_dictionary = {}

width = 50
height = 50

regals = {}
regal_no = 0

for j in range(8, 50, 6):
    for i in range(5, 20):
        regals[str(regal_no)] = Regal(regal_no, (i, j))
        regal_no += 1
        regals[str(regal_no)] = Regal(regal_no, (i, j-1))
        regal_no += 1

    for i in range(30, 45):
        regals[str(regal_no)] = Regal(regal_no, (i, j))
        regal_no += 1
        regals[str(regal_no)] = Regal(regal_no, (i, j-1))
        regal_no += 1

for i in range(100):
    article_dictionary[str(i)] = random.randint(0, regal_no-1)

checkouts = []
for i in range(4, 48, 3):
    checkouts.append((width-1, i))

shop = Shop(article_dictionary, regals, checkouts)


def agent_portrayal(agent):
    if type(agent) is RegalAgent:
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

        if agent.is_checked_up():
            portrayal["Color"] = "white"
    return portrayal


grid = CanvasGrid(agent_portrayal, width, height, width*10, height*10)

server = ModularServer(MarketModel,
                       [grid],
                       "Money Model",
                       {"agents_number": 50, "width": width, "height": height, "shop": shop})
