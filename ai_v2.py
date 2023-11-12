import numpy as np

from boards import Board, StatsBoard
from game_def import SHIPS


class StatisticalGuesser:
    NAME = "Statistical Guesser - Basic"
    HIT = 1.
    MISS = -1.
    UNKNOWN = 0.

    def __init__(self, ask_fn, ships=SHIPS, rows=12, cols=12):
        self.rows = rows
        self.cols = cols

        self.ask_fn = ask_fn
        # self.guess_board = Board(rows, cols)

        self.queued_shots = set()
        self.ships = ships

        self.shots = []
        self.hits = 0
        self.hit_board = Board(rows, cols)

    def unknown_neighbors(self, y, x):
        s = set()
        for yy in range(max(0, y - 1), min(y + 2, self.rows)):
            for xx in range(max(0, x - 1), min(x + 2, self.cols)):
                if self.hit_board.board[yy, xx] == StatisticalGuesser.UNKNOWN:
                    s.add((yy, xx))
        return s

    def mark_shot(self, y, x, was_hit):
        self.shots.append((y, x))

        # Update hit board data for this position
        if self.hit_board.board[y, x] == StatisticalGuesser.UNKNOWN:
            self.hit_board.board[y, x] = StatisticalGuesser.HIT if was_hit else StatisticalGuesser.MISS

        # Update candidate queue with neighbors, if hit
        if was_hit:
            self.hits += 1
            self.queued_shots |= self.unknown_neighbors(y, x)


    def send_shot(self, y, x):
        is_hit = self.ask_fn(y, x)
        self.mark_shot(y, x, is_hit)
        # print('Asking ', (y, x), f"(hits {self.hits})")

    def analyze(self):
        analyze_board = StatsBoard(self.rows, self.cols)
        for ship in self.ships:
            for shape in ship['shapes']:
                for y in range(0, self.rows):
                    for x in range(0, self.cols):
                        shape_copy = shape.copy()
                        if self.hit_board.can_place(y, x, shape_copy, check_proximity=False):
                            analyze_board.place(y, x, shape_copy)

        # Find most likely square to guess
        # print("Analysis board:")
        # analyze_board.print()
        indices = np.where(analyze_board.board == analyze_board.board.max())
        ymax, xmax = next(zip(indices[0], indices[1]))

        return ymax, xmax

    def get_queued(self):
        if len(self.queued_shots):
            return self.queued_shots.pop()
        return False

    def move(self):
        move = self.get_queued()
        if not move:
            move = self.analyze()

        if move in self.shots:
            print("Out of moves")
            return False

        self.send_shot(move[0], move[1])
        return True

    def print_board(self):
        self.hit_board.print()
        # self.guess_board.print()