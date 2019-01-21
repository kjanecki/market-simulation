
import tornado


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

class CustomersHandler(BaseHandler):

    def initialize(self, market_buff):
        self.market_buff = market_buff
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
        shopping_lists = {}
        for agent in self.market_buff:
            shopping_lists[agent.unique_id] = [product.name for product in agent.shopping_list]
        self.write(shopping_lists)

class ColorChangeHandler(BaseHandler):

    def initialize(self, market_buff):
        self.market_buff = market_buff
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
        agent_id = self.get_argument("id")
        for agent in self.market_buff:
            if str(agent.unique_id) == str(agent_id):
                agent.color = "black"


class AgentCountsHandler(BaseHandler):

    def initialize(self, market_buff):
        self.market_buff = market_buff
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
        self.write({"z": self.market_buff[0]})
