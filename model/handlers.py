import tornado


class CustomersHandler(tornado.web.RequestHandler):

    def initialize(self, market_buff):
        self.market_buff = market_buff

    def get(self):
        shopping_lists = {}
        for agent in self.market_buff:
            shopping_lists[agent.unique_id] = [product.name for product in agent.shopping_list]
        self.write(shopping_lists)

class ColorChangeHandler(tornado.web.RequestHandler):

    def initialize(self, market_buff):
        self.market_buff = market_buff

    def get(self):
        agent_id = self.get_argument("id")
        for agent in self.market_buff:
            print(agent.unique_id)
            if str(agent.unique_id) == str(agent_id):
                agent.color = "black"


