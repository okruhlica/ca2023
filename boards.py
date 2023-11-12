from random import randint, choice
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import numpy as np
from numpy import uint8

from game_def import SHIPS, SHIP_COUNTS


class Board:
    def __init__(self, y_size, x_size):
        self.board = np.zeros((y_size, x_size), dtype=float)
        self.cols = x_size
        self.rows = y_size

    def can_place(self, y, x, ship, check_proximity=True):
        # Determine ship matrix size
        ship_area = ship
        ship = ship[1:-1, 1:-1]
        sh_x = ship.shape[0] if len(ship.shape) == 1 else ship.shape[1]
        sh_y = 1 if len(ship.shape) == 1 else ship.shape[0]

        if y + sh_y > self.rows or x + sh_x > self.cols:
            # print('Overboard')
            return False

        # Test collision
        # test_mx = np.multiply(self.board[y:y + sh_y, x:x + sh_x], ship)
        # if test_mx.sum() != 0:
        #     # print('Collision')
        #     return False

        test_mx = np.multiply(self.board[y:y + sh_y, x:x + sh_x], ship)
        if test_mx.min() != 0 or test_mx.max() !=0:
            # print('Collision')
            return False

        if not check_proximity:
            return True

        # Test neighborhood
        bx, by = x - 1, y - 1
        if x == 0:
            ship_area = ship_area[:, 1:]
            bx += 1
        if y == 0:
            ship_area = ship_area[1:, :]
            by += 1
        if x+sh_x + 2 >= self.cols:
            ship_area = ship_area[:, :-1]

        if y+sh_y + 2 >= self.rows:
            ship_area = ship_area[:-1, :]

        test_mx = np.multiply(self.board[by:by + ship_area.shape[0], bx:bx + ship_area.shape[1]], ship_area)
        if test_mx.sum() != 0:
            # print('Too close')
            return False

        return True

    def try_place(self, y, x, ship):
        if not self.can_place(y, x, ship):
            return False
        self.place(y, x, ship)
        return True

    def place(self, y, x, ship):
        sh_x = ship.shape[1] - 2
        sh_y = ship.shape[0] - 2
        self.board[y:y + sh_y, x:x + sh_x] += ship[1:-1, 1:-1]
        return True

    def print(self):
        np.set_printoptions(precision=0)
        print(self.board)

class HitBoard(Board):

    def can_place(self,y,x,ship):
        b = self.board.copy()
        self.board[self.board < 0] = 0
        res = Board.can_place(self,y,x,ship)
        self.board=b
        return res

class StatsBoard(Board):

    def place(self, y, x, ship):
        sh_x = ship.shape[1] - 2
        sh_y = ship.shape[0] - 2
        ship[ship < 1] = 0
        self.board[y:y + sh_y, x:x + sh_x] += ship[1:-1, 1:-1]
        return True

def generate_random_board(y, x):
    b = Board(y, x)
    for ship in SHIPS:
        name = ship['name']
        count = SHIP_COUNTS[name]
        while count > 0:
            rx, ry = randint(0, b.cols - 1), randint(0, b.rows - 1)
            shipdef = choice(ship['shapes'])
            success = b.try_place(ry, rx, shipdef)
            if success:
                # print(f'Placed {name} at [{rx},{ry}].')
                count -= 1
    return b
