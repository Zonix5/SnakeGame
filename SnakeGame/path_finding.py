# path_finding.py

from astar import astar
from snake import Snake, virtual_snake
from utils import Direction, Point


def longest_path(snake: Snake)-> None | list[Point]:
    """
    Get the direction that moves it farthest away from the tail.
    :param snake: The snake object.
    :return: The direction that moves it farthest away from the tail ,or None if no direction found.
    """
    snake_pos = list(snake.snake_pos)
    head_pos = snake_pos[-1]
    dis = -1
    path = []

    for direction in Direction.directions:
        next_pos = Point(head_pos.x + direction.x, head_pos.y + direction.y)

        if snake.wall_collision:
            if snake.is_collision(next_pos):
                continue

        new_snake = virtual_snake(snake, [direction])

        if not new_snake.dead:
            path_to_tail = astar(new_snake, tail=True, move=False)
            if path_to_tail and len(path_to_tail) > dis:
                path.append(direction)
                dis = len(path_to_tail)

    if path:
        return [path[-1]]
    return None


def find_path(snake: Snake)-> list[Point]:
    """
    Path finder used in the game logic.
    :param snake: The snake object.
    :return: The path for the snake.
    """
    if path_to_food := astar(snake):
        return path_to_food

    if path := longest_path(snake):
        return path
    return [snake.direction]
