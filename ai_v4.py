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
        self.moves = 0
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
                if not (self.shot_board.is_one(y, x) and not self.miss_board.is_one(y, x)):
                    return y, x
        except IndexError:
            return None, None
        return None, None

    def reset_queue(self):
        self.queue = []
        self.sunk_ships = set()

    def avenger_sunk(self):
        return 9 in self.sunk_ships

    def analyze(self):
        count_board = CountBoard(self.rows, self.cols)
        for ship in self.fleet.ships:
            pieces = ship['size']
            if pieces > 3 and pieces in self.sunk_ships:
                continue

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
        avenger_found = self.avenger_sunk()

        def try_set_miss(y, x):
            if 0 <= y < self.rows:
                if 0 <= x < self.cols:
                    if not self.hit_board.is_one(y, x):
                        self.miss_board.set_cell(y, x, 1)

        def is_miss(y, x, default=False):
            if 0 <= y < self.rows:
                if 0 <= x < self.cols:
                    return self.miss_board.is_one(y, x)
            return default

        def is_hit(y, x, default=False):
            if 0 <= y < self.rows:
                if 0 <= x < self.cols:
                    return self.hit_board.is_one(y, x)
            return default

        def try_expand(fromy, fromx, horizontal=True, reverse=False):
            dx = 1 if horizontal else 0
            dy = 1 - dx
            if reverse:
                dx, dy = -dx, -dy

            yy, xx = fromy + dy, fromx + dx
            nexty, nextx = None, None
            steps = 0
            continues = 0
            can_expand = False

            while 0 <= xx < self.cols and 0 <= yy < self.rows and not self.miss_board.is_one(yy, xx):
                used[yy,xx] = 1.0
                if self.hit_board.is_one(yy, xx):
                    continues += 1
                elif nextx is None:
                    can_expand = True
                    nexty, nextx = yy, xx

                steps += 1
                yy += dy
                xx += dx
            return can_expand, (continues, steps, nexty, nextx)

        def find_AC(y,x):
            if 5 in self.sunk_ships and 9 in self.sunk_ships:
                return

            if not self.hit_board.is_one(y, x):
                return False

            expands, res1 = try_expand(y, x, horizontal=True)

            # Avenger carrier horizontally (or a 5)
            if res1[0] == 4:
                mark_misses = [(0,-1), (0,5), (-1,-1), (-1,0), (-1,2), (-1,4), (-1,5), (1,-1), (1,0,),(1,2), (1,4),(1,5)]
                for mark_y, mark_x in mark_misses:
                    try_set_miss(y+mark_y, x+mark_x)

                wing_positions = [(y - 1, x + 1), (y - 1, x + 3),
                                  (y + 1, x + 1), (y + 1, x + 3)] # Possible positions of wings
                wings_hit = 0
                missing_wing = -1, -1

                for ty, tx in wing_positions:
                    if is_miss(ty, tx): # By process of elimination - this can't be AC
                        self.sunk_ships.add(5) # Add the position of a sunk 5 ship
                        for tty, ttx in wing_positions:
                            try_set_miss(tty, ttx)
                        return

                    if is_hit(ty, tx): # By process of elimination - this is an AC
                        wings_hit += 1
                        for xxx in [-1, 0, 1]:
                            for yyy in [-1, 0, 1]:
                                try_set_miss(ty + yyy, tx + xxx)
                    else:
                        missing_wing = (ty, tx)

                if wings_hit > 0:
                    if missing_wing != (-1, -1):
                        self.enqueue_one(missing_wing[0], missing_wing[1], -9)
                        return
                if wings_hit == 4:
                    self.sunk_ships.add(9)

            # Inspect vertical AC/5
            expands, res2 = try_expand(y, x, horizontal=False)
            if res2[0] == 4:  # Avenger carrier or 5
                mark_misses = [(0, -1), (0, 5), (-1, -1), (-1, 0), (-1, 2), (-1, 4), (-1, 5), (1, -1), (1, 0,), (1, 2),
                               (1, 4), (1, 5)]
                for mark_x, mark_y in mark_misses:
                    try_set_miss(y + mark_y, x + mark_x)

                wing_positions = [(y + 1, x - 1), (y + 3, x - 1), (y + 1, x + 1), (y + 3, x + 1)]
                wings_hit = 0
                missing_wing = (-1, -1)

                for ty, tx in wing_positions:
                    if is_miss(ty, tx):
                        self.sunk_ships.add(5)  # By process of elimination - this is an 5-ship
                        for tty, ttx in wing_positions:
                            try_set_miss(tty, ttx)
                        return

                    if is_hit(ty, tx):
                        wings_hit += 1  # By process of elimination - this is an AC
                        for xxx in [-1, 0, 1]:
                            for yyy in [-1, 0, 1]:
                                try_set_miss(ty + yyy, tx + xxx)
                    else:
                        missing_wing = (ty, tx)

                if wings_hit > 0:
                    if missing_wing != (-1, -1):
                        self.enqueue_one(missing_wing[0], missing_wing[1], -9)
                if wings_hit == 4:
                    self.sunk_ships.add(9)

        def find_4(y, x):
            if 4 in self.sunk_ships:
                return

            can_expand, res = try_expand(y, x, True, False)
            continues, steps, nexty, nextx = res

            if is_hit(y, x-1, True) or is_hit(y-1, x, True):
                return

            if steps == 3:
                both_sides_blocked = is_miss(y, x - 1, True) and is_miss(y, x + 4, True)
                larger_ships_sunk = 9 in self.sunk_ships # and 5 in self.sunk_ships

                if nextx is not None and nextx <= x + 3:
                    self.enqueue_one(y, nextx, -4)
                    return

                if larger_ships_sunk or both_sides_blocked: # This is surely a ship
                    for dy in [-1, 1]:
                        for dx in [-1, 0, 1, 2, 3, 4]:
                            if is_hit(y+dy,x+dx, False):
                                continue
                            else:
                                try_set_miss(y+dy, x+dx)
                    self.sunk_ships.add(4)
                    return

            can_expand, res = try_expand(y, x, False, False)
            continues, steps, nexty, nextx = res

            if steps == 3:
                both_sides_blocked = is_miss(y - 1, x, True) and is_miss(y+4, x, True)
                larger_ships_sunk = 9 in self.sunk_ships

                if nexty is not None and nexty <= y + 3:
                    self.enqueue_one(nexty, x, -4)
                    return

                if larger_ships_sunk and both_sides_blocked:  # This is surely a ship
                    for dy in [-1, 0, 1, 2, 3, 4]:
                        for dx in [-1, 1]:
                            if is_hit(y+dy, x+dx, False):
                                continue
                            else:
                                 try_set_miss(y + dy, x + dx)
                    self.sunk_ships.add(4)
                    return

        def find_3(y, x):
            if 3 in self.sunk_ships:
                return

            can_expand, res = try_expand(y, x, True, False)
            continues, steps, nexty, nextx = res

            if is_hit(y, x-1, True) or is_hit(y-1, x, True):
                return

            if steps == 2:
                both_sides_blocked = is_miss(y, x - 1, True) and is_miss(y, x + 3, True)
                larger_ships_sunk = 9 in self.sunk_ships # and 5 in self.sunk_ships

                if nextx is not None and nextx <= x + 2:
                    self.enqueue_one(y, nextx, -3)
                    return

                if larger_ships_sunk or both_sides_blocked: # This is surely a ship
                    for dy in [-1, 1]:
                        for dx in [-1, 0, 1, 2, 3]:
                            if is_hit(y+dy,x+dx, False):
                                continue
                            else:
                                try_set_miss(y+dy, x+dx)
                    self.sunk_ships.add(3)
                    return

            can_expand, res = try_expand(y, x, False, False)
            continues, steps, nexty, nextx = res

            # if steps == 2:
            #     both_sides_blocked = is_miss(y - 1, x, True) and is_miss(y+3, x, True)
            #     larger_ships_sunk = 4 in self.sunk_ships
            #
            #     if nexty is not None and nexty <= y + 2:
            #         self.enqueue_one(nexty, x, -3)
            #         return
            #
            #     if larger_ships_sunk and both_sides_blocked:  # This is surely a ship
            #         for dy in [-1, 0, 1, 2, 3]:
            #             for dx in [-1, 1]:
            #                 if is_hit(y+dy, x+dx, False):
            #                     continue
            #                 else:
            #                      try_set_miss(y + dy, x + dx)
            #         self.sunk_ships.add(3)
            #         return

        def find_2(y, x):
            if 2 in self.sunk_ships:
                return

            can_expand, res = try_expand(y, x, True, False)
            continues, steps, nexty, nextx = res

            if is_hit(y, x - 1, True) or is_hit(y - 1, x, True):
                return

            if steps == 1:
                both_sides_blocked = is_miss(y, x - 1, True) and is_miss(y, x + 2, True)

                if nextx is not None and nextx <= x + 1:
                    self.enqueue_one(y, nextx, -2)
                    return

                if both_sides_blocked:  # This is surely a ship
                    for dy in [-1, 1]:
                        for dx in [-1, 0, 1, 2]:
                            if is_hit(y + dy, x + dx, False):
                                continue
                            else:
                                try_set_miss(y + dy, x + dx)
                    self.sunk_ships.add(2)
                    return

        self.reset_queue()
        used = np.zeros((self.rows, self.cols))

        # Prio 1: Detect obvious ships and potentially enqueue finishing steps
        for fn in [find_AC, find_4, find_2]:
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.hit_board.is_one(y, x) and used[y,x] == 0:
                        fn(y, x)

        # Prio 2: Detect unfinished lines in 4 directions and enqueue
        for y in range(self.rows):
            for x in range(self.cols):

                if not self.hit_board.is_one(y, x):
                    continue
                enqueue = (None, None)
                for horiz in [False, True]:
                    for reverse in [False, True]:
                        expands, res = try_expand(y, x, horizontal=horiz, reverse=reverse)
                        if expands:
                            continues, steps, nexty, nextx = res
                            if 9 in self.sunk_ships:
                                if continues > 0:
                                    enqueue = (nexty, nextx)

                            if enqueue == (None, None):
                                enqueue = (nexty, nextx)
                        if enqueue != (None, None):
                            self.enqueue_one(enqueue[0], enqueue[1], 0)
        # print(self.queue)
    def move(self):
        self.moves+=1
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
