# render.py

import pygame

from snake import Snake
from utils import Color, RGB, Point


class Render:
    CASE_SIZE = 25

    def __init__(self, size: tuple[int, int]):
        """
        Initialize the game screen for the Snake game.
        :param size: The size of the grid.
        """
        pygame.init()
        self.length, self.width = size
        self.screen = pygame.display.set_mode((self.CASE_SIZE * self.width, self.CASE_SIZE * self.length))
        pygame.display.set_caption("Snake")
        self.screen.fill(Color.WHITE)

    def set_pixel(self, pos: Point, color: Color | RGB):
        """
        Set a pixel on the grid.
        :param pos: Position of the pixel.
        :param color: Color of the pixel.
        """
        pygame.draw.rect(self.screen, color,
                         (pos.x * self.CASE_SIZE, pos.y * self.CASE_SIZE, self.CASE_SIZE, self.CASE_SIZE))

    def update_display(self, snake: Snake):
        """
        Update the display of the screen.
        :param snake: The snake object.
        """
        if pos := snake.food_pos:
            self.set_pixel(pos, Color.RED)

        max_len = len(snake.snake_pos) - 1
        for idx, pos in enumerate(snake.snake_pos):
            coef = (max_len - idx) / max_len
            r = 0
            g = 255 - 255 * coef
            b = 255 * coef
            color = RGB(r, g, b)
            self.set_pixel(pos, color)

        if pos := snake.old_tail:
            self.set_pixel(pos, Color.WHITE)

        # self.set_pixel(list(snake.snake_pos)[-1], Color.GREEN)
        pygame.display.flip()
