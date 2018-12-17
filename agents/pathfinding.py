
import bisect

import numpy as np


class Node:

    def __init__(self, previous_node, position) -> None:
        self.previous_node = previous_node
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def compute_astar_shortest_path(graph, start_pos, end_pos):

    start_node = Node(None, start_pos)
    end_node = Node(None, end_pos)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0

        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            return back_propagate_path(current_node)

        neighbor_nodes = compute_neighborhood(graph, current_node)

        for neighbor in neighbor_nodes:

            if neighbor in closed_list:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = manhattan_distance_heuristic(current_node.position, end_pos)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor in open_list:
                # for open_node in open_list:
                #     if neighbor == open_node and neighbor.g > open_node.g:
                #         continue
                continue

            bisect.insort(open_list, neighbor)


def distance_heuristic(current_pos, goal_pos):
    return ((current_pos[0] - goal_pos[0]) ** 2) + ((current_pos[1] - goal_pos[1]) ** 2)


def manhattan_distance_heuristic(current_pos, goal_pos):
    dx = abs(current_pos[0] - goal_pos[0])
    dy = abs(current_pos[1] - goal_pos[1])
    return dx + dy


def back_propagate_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.previous_node
    return path[::-1]


def compute_neighborhood(graph, current_node):
    central_point = current_node.position
    neighbors = []
    for step in [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
        new_position = (central_point[0]+step[0], central_point[1]+step[1])
        if is_in_range(new_position, graph):
            if graph[new_position] != 1:
                neighbors.append(Node(current_node, new_position))

    return neighbors


def is_in_range(pos, graph):
    return len(graph) > pos[0] >= 0 and len(graph[1]) > pos[1] >= 0
