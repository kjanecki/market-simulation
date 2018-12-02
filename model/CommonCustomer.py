from model.Customer import Customer


class CommonCustomer(Customer):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model, articles)
        self.next_article = ()

    def find_path(self):
        next_article_location = self.articles[str(self.shopping_list.pop(0))]
        x, y = self.x, self.y
        i = 1
        j = 1
        if x > next_article_location[0]:
            i = -1

        while x != next_article_location[0]:
            x = x + i
            self.step_queue.append((x, y))

        if y > next_article_location[1]:
            j = -1

        while y != next_article_location[1]:
            y = y + j
            self.step_queue.append((x, y))

    def move(self):
        next_step = self.step_queue.pop(0)
        self.x, self.y = next_step[0], next_step[1]
        self.model.grid.move_agent(self, (self.x, self.y))

    def go_to_checkout(self):
        print("Finished shopping")