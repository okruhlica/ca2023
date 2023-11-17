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

    # def enqueue_neighbors(self, y, x, priority=10):
    #     s = set()
    #     for (yy, xx) in [(y-1,x), (y+1,x), (y, x-1), (y, x+1)]:
    #             if 0 <= yy < self.rows and \
    #                 0 <= xx < self.cols and \
    #                     not self.shot_board.is_one(yy, xx):
    #                 self.enqueue_one(yy, xx, priority)

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
            # self.enqueue_neighbors(y, x, 10)
        elif response.cell == '.':
            self.miss_board.set_cell(y, x, 1)


    def find_lines(self):
        def try_set_miss(y,x):
            if 0 <= y < self.rows:
                if 0 <= x < self.cols:
                    self.miss_board.set_cell(y,x,1)

        def is_miss(y,x):
            if 0 <= y < self.rows:
                if 0 <= x < self.cols:
                    return self.miss_board.is_one(y, x)
            return False

        def is_hit(y,x):
            if 0 <= y < self.rows:
                if 0 <= x < self.cols:
                    return self.hit_board.is_one(y, x)
            return False
        def try_expand(fromy,fromx, horizontal=True, reverse = False):
            dx = 1 if horizontal else 0
            dy = 1 - dx
            if reverse:
                dx, dy = -dx, -dy

            yy, xx = fromy+dy,fromx+dx
            nexty, nextx = None, None
            steps = 0
            continues = 0
            can_expand = False

            while 0 <= xx < self.cols and 0 <= yy < self.rows and not self.miss_board.is_one(yy, xx):
                if self.hit_board.is_one(yy, xx):
                    continues+=1
                elif nextx is None:
                    can_expand = True
                    nexty, nextx = yy, xx
                steps+=1
                yy+=dy
                xx+=dx
            return can_expand, (continues, steps, nexty, nextx)

        lines = []
        used = np.zeros((self.rows, self.cols))
        for y in range(self.rows):
            for x in range(self.cols):
                if used[y, x]:
                    continue

                if self.hit_board.is_one(y,x):
                    expands, res1 = try_expand(y, x, horizontal=True)
                    if res1[0] == 4: # Avenger carrier or 5
                        try_set_miss(y, x - 1)
                        try_set_miss(y, x + 5)

                        try_set_miss(y - 1, x - 1)
                        try_set_miss(y - 1, x)
                        try_set_miss(y - 1, x + 2)
                        try_set_miss(y - 1, x + 4)
                        try_set_miss(y - 1, x + 5)

                        try_set_miss(y + 1, x - 1)
                        try_set_miss(y + 1, x)
                        try_set_miss(y + 1, x + 2)
                        try_set_miss(y + 1, x + 4)
                        try_set_miss(y + 1, x + 5)

                        av = [(y-1,x+1),(y-1,x+3),(y+1,x+1),(y+1,x+3)]
                        for ty, tx in av:
                            if is_miss(ty,tx):
                                for tty, ttx in av:
                                    try_set_miss(tty, ttx)
                            if is_hit(ty, tx):
                                pass #todo


                    expands, res2 = try_expand(y, x, horizontal=False)
                    if res2[0] == 4: # Avenger carrier or 5
                        try_set_miss(y - 1, x)
                        try_set_miss(y + 5, x)

                        try_set_miss(y - 1, x - 1)
                        try_set_miss(y, x - 1)
                        try_set_miss(y, x + 1)

                        try_set_miss(y + 2, x - 1)
                        try_set_miss(y + 2, x + 1)

                        try_set_miss(y + 4, x - 1)
                        try_set_miss(y + 4, x + 1)

                        try_set_miss(y + 5, x - 1)
                        try_set_miss(y + 5, x + 1)

                        av = [(y + 1, x - 1), (y + 3, x - 1), (y + 1, x + 1), (y + 3, x + 1)]
                        for ty, tx in av:
                            if is_miss(ty, tx):
                                for tty, ttx in av:
                                    try_set_miss(tty, ttx)
                            if is_hit(ty, tx):
                                pass  # todo

                    lines.append(res1)
                    lines.append(res2)
                    expands, res = try_expand(y, x, horizontal=True, reverse=True)
                    if expands:
                        lines.append(res)
                    expands, res = try_expand(y, x, horizontal=False, reverse=True)
                    if expands:
                        lines.append(res)

        lines.sort(reverse=True)
        while len(lines):
            c, l, y, x = lines.pop()
            if c < 5 and y is not None and not self.shot_board.is_one(y, x) and not self.miss_board.is_one(y, x):
                self.enqueue_one(y, x, priority=1)
                return

    def move(self):
        self.find_lines()
        # self.analyze_board()

        y, x = self.dequeue_new()
        if y is None or x is None:
            y, x = self.analyze()

        if (y, x) in self.shots:
            print(f"Out of moves after {self.hits} hits.")
            return False

        response = self.send_shot(y, x)
        self.update_cell(y, x, response)
        return True
