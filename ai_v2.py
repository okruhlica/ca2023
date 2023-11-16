import numpy as np

from boards import ZeroOneBoard, CountBoard
from ship import ShipShapeType


class StatisticalGuesser:

    def __init__(self, ask_fn, gamedef):
        self.rows = gamedef.rows
        self.cols = gamedef.cols
        self.fleet = gamedef.fleet

        self.ask_fn = ask_fn

        self.shots = []
        self.queued_shots = set()

        # self.needed = gamedef.hits_needed
        self.hits = 0
        self.hit_board = ZeroOneBoard(self.rows, self.cols)
        self.miss_board = ZeroOneBoard(self.rows, self.cols)

    def unknown_neighbors(self, y, x):
        s = set()
        for yy in range(max(0, y - 1), min(y + 2, self.rows)):
            for xx in range(max(0, x - 1), min(x + 2, self.cols)):
                if not self.hit_board.is_one(yy, xx):
                    s.add((yy, xx))
        return s

    def send_shot(self, y, x):
        self.shots.append((y, x))
        response = self.ask_fn(y, x)


        # Update candidate queue with neighbors, if hit
        if response.cell == 'X':
            self.hits += 1
            self.hit_board.set_cell(y, x, 1)
            self.queued_shots |= self.unknown_neighbors(y, x)
        elif response.cell == '.':
            self.miss_board.set_cell(y, x, 1)
            self.hit_board.set_cell(y, x, 1)

    def analyze(self):
        count_board = CountBoard(self.rows, self.cols)
        for ship in self.fleet.ships:
            for ship_variant in ship['variants']:
                ship_only = ship_variant.get_shape(ShipShapeType.SHIP_TRIMMED)
                for y in range(0, self.rows):
                    for x in range(0, self.cols):
                        if self.hit_board.can_place(y, x, ship_only.copy()):
                            count_board.place(y, x, ship_only.copy())

        best_y, best_x = count_board.max_index()
        return best_y, best_x

        # analyze_board = StatsBoard(self.rows, self.cols)
        # for ship in self.ships:
        #     for shape in ship['shapes']:
        #         for y in range(0, self.rows):
        #             for x in range(0, self.cols):
        #                 shape_copy = shape.copy()
        #                 if self.hit_board.can_place(y, x, shape_copy, check_proximity=False):
        #                     analyze_board.place(y, x, shape_copy)
        #
        #
        # indices = np.where(analyze_board.board == analyze_board.board.max())
        # ymax, xmax = next(zip(indices[0], indices[1]))

    def move(self):
        move = self.get_queued()
        if not move:
            move = self.analyze()

        if move in self.shots:
            print(f"Out of moves after {self.hits} hits.")
            return False

        self.send_shot(move[0], move[1])
        return True

    def get_queued(self):
        if len(self.queued_shots):
            return self.queued_shots.pop()
        return False

    def print_board(self):
        self.hit_board.print()
        # self.guess_board.print()
