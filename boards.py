# from random import randint, choice
#
# import numpy as np
#
#
# class Board:
#     def __init__(self, y_size, x_size):
#         self.board = np.zeros((y_size, x_size), dtype=float)
#         self.cols = x_size
#         self.rows = y_size
#
#     def can_place(self, y, x, ship, check_proximity=True, fit_mask=False):
#         # Todo rethink this whole proc
#
#         # Determine ship matrix size
#         ship_area = ship
#         ship = ship[1:-1, 1:-1]
#         sh_x = ship.shape[0] if len(ship.shape) == 1 else ship.shape[1]
#         sh_y = 1 if len(ship.shape) == 1 else ship.shape[0]
#
#         if y + sh_y > self.rows or x + sh_x > self.cols:
#             # print('Overboard')
#             return False
#
#         # board = np.subtract(, fit_mask) if fit_mask is not False else self.board
#         if fit_mask is False:
#             board = self.board
#         else:
#             board = self.board.copy()
#             mask = np.zeros(board.shape)
#             mask[y:y + fit_mask.shape[0], x:x + fit_mask.shape[1]] += fit_mask
#             # fit_mask.resize(board.shape, refcheck=False)
#             board = np.subtract(board, mask)
#
#         # test_mx = np.multiply(board[y:y + sh_y, x:x + sh_x], ship)
#         # if test_mx.min() != 0 or test_mx.max() != 0:
#         #     return False
#
#         test_mx = np.add(board[y:y + sh_y, x:x + sh_x], ship)
#         if test_mx.sum() != ship.sum():
#             return False
#
#         if not check_proximity:
#             return True
#
#         # Test neighborhood
#         bx, by = x - 1, y - 1
#         if x == 0:
#             ship_area = ship_area[:, 1:]
#             bx += 1
#         if y == 0:
#             ship_area = ship_area[1:, :]
#             by += 1
#         if x + sh_x + 2 >= self.cols:
#             ship_area = ship_area[:, :-1]
#
#         if y + sh_y + 2 >= self.rows:
#             ship_area = ship_area[:-1, :]
#
#         test_mx = np.multiply(board[by:by + ship_area.shape[0], bx:bx + ship_area.shape[1]], ship_area)
#         if test_mx.sum() != 0:
#             # print('Too close')
#             return False
#
#         return True
#
#     def try_place(self, y, x, ship):
#         if not self.can_place(y, x, ship):
#             return False
#         self.place(y, x, ship)
#         return True
#
#     def place(self, y, x, ship):
#         sh_x = ship.shape[1] - 2
#         sh_y = ship.shape[0] - 2
#         self.board[y:y + sh_y, x:x + sh_x] += ship[1:-1, 1:-1]
#         return True
#
#     def print(self):
#         np.set_printoptions(precision=0)
#         print(self.board)
#
#
# class HitBoard(Board):
#
#     def can_place(self, y, x, ship):
#         b = self.board.copy()
#         self.board[self.board < 0] = 0
#         res = Board.can_place(self, y, x, ship)
#         self.board = b
#         return res
#
#
# class StatsBoard(Board):
#
#     def place(self, y, x, ship):
#         sh_x = ship.shape[1] - 2
#         sh_y = ship.shape[0] - 2
#         ship[ship < 1] = 0
#         self.board[y:y + sh_y, x:x + sh_x] += ship[1:-1, 1:-1]
#         return True
#
import os
from random import choice, randint

import numpy as np

from ship import Ship, ShipShapeType


def _get_shape_2d(obj):
    if len(obj.shape) == 1:
        return 1 if obj.shape[0] > 0 else 0, obj.shape[0]
    return obj.shape[0], obj.shape[1]


class ZeroOneBoard:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.board = np.zeros((rows, cols))

    def copy(self):
        other = ZeroOneBoard(self.rows, self.cols)
        other.board = self.board.copy()
        return other

    def reset(self):
        self.board[:, :] = 0

    def fits(self, y, x, obj):
        if y < 0 or x < 0:
            return False

        objrows, objcols = _get_shape_2d(obj)
        if x + objcols <= self.cols and y + objrows <= self.rows:
            return True

        return False

    def can_place(self, y, x, shape):
        if not self.fits(y, x, shape):
            return False

        shape_h, shape_w = _get_shape_2d(shape)
        return np.multiply(self.board[y:y + shape_h, x:x + shape_w], shape).sum() == 0

    def place(self, y, x, shape):
        if not self.fits(y, x, shape):
            return False

        shape_h, shape_w = _get_shape_2d(shape)
        self.board[y:y + shape_h, x:x + shape_w] += shape
        return True

    def from_str(self, s, line_delim=os.linesep):
        self.rows, self.cols = len(s.split(line_delim)), len(s.split(line_delim)[0])
        self.board = np.zeros((self.rows, self.cols))

        for y, line in enumerate(s.split(line_delim)):
            for x, char in enumerate(line):
                self.board[y, x] = 1 if char == '1' else 0

    def __str__(self):
        s = ''
        for y in range(self.rows):
            for x in range(self.cols):
                s += '1' if self.board[y, x] == 1 else '0'
            s += os.linesep
        return s

    def is_one(self, y, x):
        return self.board[y, x] == 1

    def set_cell(self, y, x, val):
        self.board[y, x] = val

    def ones(self):
        return self.board.sum()

class CountBoard:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.board = np.zeros((rows, cols))

    def place(self, y, x, obj):
        sh_h, sh_w = obj.shape
        self.board[y:y+sh_h, x:x+sh_w]+=obj

    def max(self):
        return self.board.max()
    def max_index(self):
        indices = np.where(self.board == self.max())
        ymax, xmax = next(zip(indices[0], indices[1]))
        return ymax, xmax
    def reset(self):
        self.board = np.zeros((self.rows, self.cols))
