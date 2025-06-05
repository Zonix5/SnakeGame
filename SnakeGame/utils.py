# utils.py

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Vector2D = namedtuple('Vector2D', ['x', 'y'])
RGB = namedtuple('RGB', ['r', 'g', 'b'])


class Direction:
    UP = Vector2D(1, 0)
    DOWN = Vector2D(-1, 0)
    LEFT = Vector2D(0, -1)
    RIGHT = Vector2D(0, 1)

    directions = [UP, DOWN, LEFT, RIGHT]

    @staticmethod
    def is_opposite(dir1: Vector2D, dir2: Vector2D)-> bool:
        """
        Check if two directions are opposite.
        :param dir1: First direction.
        :param dir2: Second direction.
        :return: True if they are opposite else False
        """
        return dir1 == (-dir2.x, -dir2.y)


class Color:
    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    WHITE = RGB(255, 255, 255)


def manhattan_distance(pt1, pt2)-> int:
    """
    Get the manhattan distance of two point.
    :param pt1: First point.
    :param pt2: Second point.
    :return: The manhattan distance of the two point.
    """
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
