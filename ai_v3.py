import numpy as np

from boards import Board, StatsBoard
from game import FireResponse, empty_fire_response


class StatisticalGuesser2:
    NAME = "Statistical Guesser - Rookie"
    HIT = 1.
    MISS = -1.
    UNKNOWN = 0.

    def __init__(self, ask_fn, gamedef):
        self.rows = gamedef.rows
        self.cols = gamedef.cols
        self.ships = gamedef.fleet

        self.ask_fn = ask_fn

        self.shots = []
        self.queued_shots = set()

        self.needed = gamedef.hits_needed
        self.hits = 0
        self.hit_board = Board(self.rows, self.cols)
        self.response = empty_fire_response(self.rows, self.cols)


    def construct_board(self):
        '''
        Constructs the hit board from last response string.
        :return: Board instance.
        '''
        _CELL_CHAR_TO_INT = {'*': self.UNKNOWN, '.': self.MISS, 'X': self.HIT}
        EMPTY_BOARD_STR = '*' * (self.cols * self.rows)

        board_str = EMPTY_BOARD_STR if self.response is None else self.response.grid
        hit_board = Board(self.rows, self.cols)

        pos = 0
        for y in range(self.rows):
            for x in range(self.cols):
                hit_board.board[y, x] = _CELL_CHAR_TO_INT[board_str[pos]]
                pos += 1
        return self.hit_board

    def make_move(self):
        if self.response.finished:
            return False

        ships = identify_ships(hit_board, ships=self.ships)

        self.analyze_board(self.response)
        self.pick_move()
        self.fire()


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
        self.response = self.ask_fn(y, x)
        is_hit = self.response.cell == 'X'
        self.mark_shot(y, x, is_hit)

    def analyze(self):
        analyze_board = StatsBoard(self.rows, self.cols)
        for ship in self.ships:
            for shape in ship['shapes']:
                for y in range(0, self.rows):
                    for x in range(0, self.cols):
                        shape_copy = shape.copy()
                        if self.hit_board.can_place(y, x, shape_copy, check_proximity=False):
                            analyze_board.place(y, x, shape_copy)


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