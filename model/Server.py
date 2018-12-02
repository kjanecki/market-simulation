import random

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from model.MarketModel import MarketModel

article_dictionary = {}

for i in range(100):
    article_dictionary[str(i)] = (random.randint(10, 40), random.randint(10, 40))


def agent_portrayal(agent):
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
                       {"agents_number": 30, "width": 50, "height": 50, "articles": article_dictionary})
