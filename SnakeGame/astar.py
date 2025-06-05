# astar.py

import heapq

from snake import Snake, virtual_snake
from utils import Point, Vector2D, manhattan_distance, Direction


class Node:
    def __init__(self, pos: Point,
                 snake_pos: list[Point],
                 direction: Vector2D = None,
                 parent=None,
                 g_cost: int = 0,
                 h_cost: int = 0):
        """
        Create a node.
        :param pos: Position of the snake's head.
        :param snake_pos: Position of the snake.
        :param direction: Direction of the snake.
        :param parent: Parent of the node.
        :param g_cost: How many steps from the start point.
        :param h_cost: Distance from the goal.
        """
        self.pos = pos
        self.direction = direction
        self.g_cost = g_cost
        self.snake_pos = snake_pos
        self.parent = parent
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def __eq__(self, other) -> bool:
        """
        Compare node with another.
        :param other: The other node.
        :return: True if they have the same pos and g_cost else False.
        """
        return (self.pos == other.pos and
                self.g_cost == other.g_cost)

    def __lt__(self, other)-> bool:
        """
        Compare two nodes based on their f_cost and h_cost.
        :param other: The other node.
        :return: True if the f_cost of this instance is less than the f_cost of the other instance,
             or if the f_cost values are equal, True if the h_cost of this instance is less
             than the h_cost of the other instance. Otherwise, returns False
        """
        if self.f_cost == other.f_cost:
            return self.h_cost < other.h_cost
        return self.f_cost < other.f_cost



def astar(snake: Snake, tail: bool = False, move: bool = True) -> None | list[Point]:
    """
    Get a path trought the food or tail for the snake.
    :param snake: Snake object.
    :param tail: True if the goal is the tail.
    :param move: True make the path anticipate the snake movement.
    :return: The path trought the food or tail, or None if no path found.
    """
    max_g = snake.length * snake.width * 2
    start = snake.snake_pos[-1]
    if not tail:
        goal = snake.food_pos
    else:
        goal = snake.snake_pos[0]

    open_list = []
    closed_set = set()

    start_h = manhattan_distance(start, goal)
    start_node = Node(
        start,
        list(snake.snake_pos),
        h_cost=start_h
    )

    heapq.heappush(open_list, start_node)
    directions = Direction.directions

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add((current_node.pos, current_node.g_cost))

        if current_node.g_cost >= max_g:
            continue

        if current_node.pos == goal:
            path = []
            while current_node.parent:
                path.append(current_node.direction)
                current_node = current_node.parent

            path = path[::-1]
            if not tail:
                v_snake = virtual_snake(snake, path)
                path_to_tail = astar(v_snake, tail=True, move=False)
                if path_to_tail:
                    return path
                continue
            return path

        for direction in directions:
            x, y = current_node.pos.x + direction.x, current_node.pos.y + direction.y
            next_pos = Point(x, y)
            if snake.wall_collision:
                temp_snake = snake.copy()
                temp_snake.snake_pos = current_node.snake_pos
                if temp_snake.is_collision(next_pos):
                    continue
            else:
                x = x % snake.width
                y = y % snake.length
                next_pos = Point(x, y)

            if next_pos in current_node.snake_pos[1:]:
                continue

            if (next_pos, current_node.g_cost + 1) in closed_set:
                continue

            snake_pos = current_node.snake_pos.copy()
            if move:
                snake_pos.pop(0)
            snake_pos.append(next_pos)

            g_cost = current_node.g_cost + 1
            h_cost = manhattan_distance(next_pos, goal)

            next_node = Node(
                pos=next_pos,
                snake_pos=snake_pos,
                direction=direction,
                parent=current_node,
                g_cost=g_cost,
                h_cost=h_cost
            )

            existing_node = None
            for node in open_list:
                if node.pos == next_pos:
                    existing_node = node
                    break

            if existing_node is None:
                heapq.heappush(open_list, next_node)
            elif next_node.g_cost < existing_node.g_cost:
                open_list.remove(existing_node)
                heapq.heapify(open_list)
                heapq.heappush(open_list, next_node)
    return None
