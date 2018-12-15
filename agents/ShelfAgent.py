from agents.PassiveAgent import PassiveAgent


class ShelfAgent(PassiveAgent):

    def __init__(self, unique_id, model, shelf):
        super().__init__(unique_id, model)
        self.shelf = shelf

    def get_location(self):
        return self.shelf.location
