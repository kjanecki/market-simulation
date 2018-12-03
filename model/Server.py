import random

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Shop.Shop import Shop
from Shop.Regal import Regal
from agents.RegalAgent import RegalAgent
from model.MarketModel import MarketModel

article_dictionary = {}

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

shop = Shop(article_dictionary, regals, None)


def agent_portrayal(agent):
    if type(agent) is RegalAgent:
        portrayal = {"Shape": "rect",
                     "Color": "black",
                     "Filled": "true",
                     "Layer": 0,
                     "w": 0.9,
                     "h": 0.9}
    else:
        portrayal = {"Shape": "circle",
                     "Color": "red",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.5}
    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

server = ModularServer(MarketModel,
                       [grid],
                       "Money Model",
                       {"agents_number": 30, "width": 50, "height": 50, "shop": shop})
