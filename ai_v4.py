import heapq

import numpy as np

from boards import ZeroOneBoard, CountBoard
from ship import ShipShapeType


class StatisticalGuesserHunt:

    def __init__(self, ask_fn, gamedef):
        self.rows = gamedef.rows
        self.cols = gamedef.cols
        self.fleet = gamedef.fleet
        self.sunk_ships = set()

        self.ask_fn = ask_fn

        self.shots = []
        self.queue = []

        self.hits = 0
        self.shot_board = ZeroOneBoard(self.rows, self.cols)
        self.hit_board = ZeroOneBoard(self.rows, self.cols)
        self.miss_board = ZeroOneBoard(self.rows, self.cols)

    def shots_queued(self):
        return len(self.queue) > 0

    def enqueue_one(self, y, x, priority):
        heapq.heappush(self.queue, (priority, y, x))

    def dequeue_new(self):
        try:
            while len(self.queue):
                p, y, x = heapq.heappop(self.queue)
                if not (self.shot_board.is_one(y, x) or self.miss_board.is_one(y, x)):
                    return y, x
        except IndexError:
            return None, None
        return None, None

    def enqueue_neighbors(self, y, x, priority=10):
        s = set()
        for yy in range(max(0, y - 1), min(y + 2, self.rows)):
            for xx in range(max(0, x - 1), min(x + 2, self.cols)):
                if not self.shot_board.is_one(yy, xx):
                    self.enqueue_one(yy, xx, priority)

    def analyze(self):
        count_board = CountBoard(self.rows, self.cols)
        for ship in self.fleet.ships:
            for ship_variant in ship['variants']:
                ship_only = ship_variant.get_shape(ShipShapeType.SHIP_TRIMMED)
                for y in range(0, self.rows):
                    for x in range(0, self.cols):
                        if self.shot_board.can_place(y, x, ship_only.copy()):
                            count_board.place(y, x, ship_only.copy())

        best_y, best_x = count_board.max_index()
        return best_y, best_x

    def analyze_board(self):
        return
        search_ship = None
        for ship in self.fleet.ships:
            if ship['priority'] in self.sunk_ships:
                continue

            for ship_variant in ship['variants']:
                obj = ship_variant.get_shape(ShipShapeType.SHIP_TRIMMED)
                sv_h, sv_w = obj.shape
                for y in range(self.rows - sv_h):
                    for x in range(self.cols - sv_w):
                        if np.multiply(self.hit_board.board[y:y + sv_h, x:x + sv_w], obj).sum() == ship['size']:
                            if max(self.undiscovered_ships) == ship['size']:
                                self.dequeue_all(y, x, ship['priority'])
                                self.mark_all(y, x, ship_variant)
                            # self.enqueue_neighbors(y, x, ship['priority'])
                            print(f"Ship {ship['name']} found!")

    def send_shot(self, y, x):
        self.shots.append((y, x))
        self.shot_board.set_cell(y, x, 1)
        return self.ask_fn(y, x)

    def update_cell(self, y, x, response):
        if response.cell == 'X':
            self.hits += 1
            self.hit_board.set_cell(y, x, 1)
            self.enqueue_neighbors(y, x, 10)
        elif response.cell == '.':
            self.miss_board.set_cell(y, x, 1)

    def move(self):
        self.analyze_board()

        y, x = self.dequeue_new()
        if y is None or x is None:
            y, x = self.analyze()

        if (y, x) in self.shots:
            print(f"Out of moves after {self.hits} hits.")
            return False

        response = self.send_shot(y, x)
        self.update_cell(y, x, response)
        return True
