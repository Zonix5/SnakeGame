# snake.py

import random
from collections import deque

from utils import Direction, Point, Vector2D


class Snake:
    def __init__(self,
                 size: tuple[int, int],
                 snake_pos: list[Point],
                 wall_collision: bool = False,
                 old_direction: Vector2D = Direction.RIGHT,
                 food_pos : Point = None):
        """
        Create snake object.
        :param size: The size of the grid.
        :param snake_pos: Initals position of the snake.
        :param wall_collision: Enable/disable the wall collision.
        :param old_direction: The previous direction of the snake.
        :param food_pos: The position of the food.
        """

        self.length, self.width = size
        self.all_pos = {Point(x, y) for x in range(self.width)
                        for y in range(self.length)}
        self.wall_collision = wall_collision
        self.snake_pos = deque(snake_pos, len(self.all_pos))
        self.score = 0
        self.dead = False
        self.old_tail = False
        self.food_pos = food_pos if food_pos is not None else self.get_food()
        self.direction = self.old_direction = old_direction

    def get_food(self) -> None | Point:
        """
        Get a position for the food.
        :return: Postion for the food.
        """
        available_positions = self.all_pos - set(self.snake_pos)
        if not available_positions:
            return None
        return random.choice(list(available_positions))

    def move_foward(self, direction: Vector2D) -> Point:
        """
        Move the head of the snake in the specified direction.
        :param direction: The direction in which the snake should move.
        :return: The new position of the snake's head.
        """
        head = self.snake_pos[-1]

        if Direction.is_opposite(direction, self.old_direction):
            return Point(head.x + self.old_direction.x, head.y + self.old_direction.y)

        self.old_direction = direction
        return Point(head.x + direction.x, head.y + direction.y)

    def change_side(self, new_head: Point) -> Point:
        """
        Usage if wall_collision is False. Move the head on the other side of the grid.
        :param new_head: The new position for the snake's head.
        :return: The updated position of the snake's head.
        """
        x = new_head.x % self.width
        y = new_head.y % self.length
        return Point(x, y)

    def is_collision(self, new_head: Point) -> bool:
        """
        Check for collisions.
        :param new_head: The new position for the snake's head.
        :return: True if collision else False.
        """
        if self.wall_collision:
            if not (0 <= new_head.x < self.width and 0 <= new_head.y < self.length):
                return True
        return new_head in list(self.snake_pos)[1:]

    def run(self, direction: Vector2D)-> bool:
        """
        Snake game logic. Make the snake do one step on the specified direction.
        :param direction: The direction in which the snake should move.
        :return: True is the snake still alive else False.
        """
        new_head = self.move_foward(direction)

        if not self.wall_collision:
            new_head = self.change_side(new_head)

        if self.is_collision(new_head):
            self.dead = True
            return False

        self.snake_pos.append(new_head)

        if new_head == self.food_pos:
            self.score += 1
            self.old_tail = False
            self.food_pos = self.get_food()
            if self.food_pos is None:
                self.dead = True
                return False
        else:
            self.old_tail = self.snake_pos.popleft()

        return True

    def copy(self)-> 'Snake':
        """
        Create a copy of the snake.
        :return: The copy of the snake.
        """
        return Snake(
            size=(self.length, self.width),
            snake_pos=list(self.snake_pos),
            wall_collision=self.wall_collision,
            old_direction=self.old_direction,
            food_pos=self.food_pos
        )


def virtual_snake(snake: Snake, path: list[Vector2D] = None)-> Snake:
    """
    Create a copy of the snake and make it follow a path.
    :param snake: The snake object.
    :param path: The path to follow.
    :return: A snake copy with updated position.
    """
    v_snake = snake.copy()
    if path:
        for direction in path:
            v_snake.run(direction)
            if v_snake.dead:
                break

    return v_snake
