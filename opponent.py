import numpy as np

from API import FireResponse
from boards import ZeroOneBoard


class MockOpponent:

    def __init__(self, board):
        self.ship_board = board
        self.rows, self.cols = self.ship_board.rows, self.ship_board.cols

        self.hit_board = np.zeros((self.rows, self.cols))
        self.miss_board = np.zeros((self.rows, self.cols))

        self.shots = set()

    def stringify_state(self):
        def stringify_cell(y, x):
            hit = self.hit_board[y, x] == 1
            miss = self.miss_board[y, x] == 1

            if not hit and not miss:
                return '*'
            elif hit:
                return 'X'
            elif miss:
                return '.'

        s = ''
        for y in range(self.rows):
            for x in range(self.cols):
                s += stringify_cell(y, x)
        return s

    def remaining(self):
        return self.ship_board.ones()

    def finished(self):
        return self.remaining() <= 0

    def fire_at(self, y, x):
        result = True
        cell = ''

        if self.finished():
            finished = True
        elif (y, x) in self.shots:
            result = False
        elif not (0 <= x < self.cols and 0 <= y < self.rows):
            result = False

        self.shots.add((y, x))

        if result:
            if self.ship_board.is_one(y, x):
                self.hit_board[y, x] = 1
                self.ship_board.set_cell(y, x, 0)
                cell = 'X'
            else:
                self.miss_board[y, x] = 1
                cell = '.'

        return FireResponse(grid=self.stringify_state(),
                            cell=cell,
                            result=result,
                            avengerAvailable=False,
                            mapId=1,
                            mapCount=1,
                            moveCount=len(self.shots),
                            finished=self.remaining() <= 0)

    # def __init__(self, gamedef):
    #     self.gamedef = gamedef
    #     self.board = generate_random_board(gamedef)
    #     self.board.board[self.board.board < 1] = 0
    #     self.hits = np.zeros((gamedef.rows, gamedef.cols))
    #     self.misses = np.zeros((gamedef.rows, gamedef.cols))
    #     self.moves = 0
    #
    # def to_str(self):
    #     def stringify_cell(hit, miss):
    #         if hit == 0 and miss == 0:
    #             return '*'
    #         elif hit == 1:
    #             return 'X'
    #         elif miss == 1:
    #             return '.'
    #
    #     s = ''
    #     for y in range(self.gamedef.rows):
    #         for x in range(self.gamedef.cols):
    #             s += stringify_cell(self.hits[y, x], self.misses[y, x])
    #     return s
    #
    # def fire(self, y, x):
    #     self.moves += 1
    #     if self.board.board[y, x] == 1:
    #         self.hits[y, x] = 1
    #     else:
    #         self.misses[y, x] = 1
    #
    #     grid = self.to_str()
    #     cell = grid[y*self.gamedef.rows + x]
    #     result = True
    #     avenger = False
    #     map_id = 0
    #     map_count = 1
    #     move_count = self.moves
    #     is_finished = self.finished()
    #
    #     return FireResponse(grid=grid, cell=cell,
    #                         result=result, avengerAvailable=avenger,
    #                         mapId=map_id, mapCount=map_count,
    #                         moveCount=move_count,
    #                         finished=is_finished)
    #
    #
    # def finished(self):
    #     return np.array_equal(self.board.board, self.hits)
    #
    # def print_board(self):
    #     self.board.print()
