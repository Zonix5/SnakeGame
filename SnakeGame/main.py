# main.py

import _thread
import time

from path_finding import find_path
from render import Render
from snake import Snake, virtual_snake
from utils import Point

state = []
lock = _thread.allocate_lock()


def preprocess_path(snake: Snake):
    """
    Precompute paths for a virtual snake to simulate its movements.
    :param snake: The snake object.
    """
    global state
    v_snake = virtual_snake(snake)

    while not v_snake.dead:
        path = find_path(v_snake)
        with lock:
            state.append((v_snake.food_pos, path))

        for direction in path:
            v_snake.run(direction)

def main():
    """
    Run the Snake game, handling movement and rendering.

    Initializes the game, starts path preprocessing in a separate thread,
    and updates the game display until the snake dies.
    """
    global state
    snake = Snake(size=(8, 8), snake_pos=[Point(0, 0), Point(0, 1), Point(0, 2)], wall_collision=False)
    render = Render((snake.length, snake.width))
    _thread.start_new_thread(preprocess_path, (snake,))

    while not snake.dead:
        if not state:
            continue

        with lock:
            actual_state = state.pop(0)

        food_pos, path = actual_state
        snake.food_pos = food_pos
        render.update_display(snake)
        for direction in path:
            snake.run(direction)
            snake.food_pos = food_pos
            render.update_display(snake)
            time.sleep(0.05)

    print('Score : ', snake.score)


if __name__ == '__main__':
    main()
