from agents.PassiveAgent import PassiveAgent


class ShelfAgent(PassiveAgent):

    def __init__(self, unique_id, model, regal):
        super().__init__(unique_id, model)
        self.regal = regal

    def get_location(self):
        return self.regal.location
