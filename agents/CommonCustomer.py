import random

from agents.Customer import Customer


class CommonCustomer(Customer):

    def __init__(self, unique_id, model, articles):
        super().__init__(unique_id, model, articles)
        self.next_article = ()

    def find_path(self):
        next_article_location = self.model.shop.regals[str(self.articles[str(self.shopping_list.pop(0))])].location
        prev_pos = (self.x, self.y)
        waypoints = self.compute_waypoints(prev_pos, next_article_location)
        for next_pos in waypoints:
            self.compute_rectlinear_path(prev_pos, next_pos)
            prev_pos = next_pos

    def compute_waypoints(self, start_position, end_position):
        p = self.walk_along_regal(start_position, end_position)
        p2 = self.walk_aside_regal(p, end_position)
        p3 = (end_position[0], p2[1])
        p4 = self.walk_to_shelf(end_position)

        return [p, p2, p3, p4, p3]

    def walk_along_regal(self,  start_position, end_position):
        width = self.model.grid.width
        rand = random.randint(-1, 1)
        return round(width/2)+rand, start_position[1]

    def walk_aside_regal(self, start_position, end_position):
        i = 2
        if end_position[1] % 2 != 0:
            i = -1
        return start_position[0], end_position[1] + i

    def walk_to_shelf(self, end_position):
        if end_position[1] % 2 != 0:
            return end_position[0], end_position[1]-1
        else:
            return end_position[0], end_position[1]+1


    def compute_rectlinear_path(self, p1, p2):
        x, y = p1[0], p1[1]
        i = 1
        if x > p2[0]:
            i = -1
        while x != p2[0]:
            x += i
            self.step_queue.append((x, y))

        i = 1
        if y > p2[1]:
            i = -1
        while y != p2[1]:
            y += i
            self.step_queue.append((x, y))

    def move(self):
        next_step = self.step_queue.pop(0)
        self.x, self.y = next_step[0], next_step[1]
        self.model.grid.move_agent(self, (self.x, self.y))

    def go_to_checkout(self):
        print("Finished shopping")

