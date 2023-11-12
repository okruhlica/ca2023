import numpy as np
from boards import generate_random_board


def play_random_games(engine, opponent, gamedef, iterations=40):
    sum_turns = 0.0
    for game in range(iterations):
        print(f"Game #{game}")
        turns = 0
        p0 = engine(gamedef)
        p1 = opponent(p0.fire, gamedef)

        while not p0.finished():
            turns += 1.0
            if not p1.move():
                break

        if p1.hits != gamedef.hits_needed:
            print(f"!ASSERTION ERROR! ({p1.hits}/9 hits)")
            print("Game:")
            p0.print_board()
            print("Guessboard:")
            p1.print_board()
            return
        sum_turns += turns
    return sum_turns / iterations


class FireResponse:
    def __init__(self, grid, cell, result, avengerAvailable=False, mapId=0, mapCount=1, moveCount=10, finished=False):
        self.grid = grid
        self.cell = cell
        self.result = result
        self.avenger_available = avengerAvailable
        self.map_id = mapId
        self.map_count = mapCount
        self.move_count = moveCount
        self.game_finished = finished


class GameEngine:
    def __init__(self, gamedef):
        self.gamedef = gamedef
        self.board = generate_random_board(gamedef)
        self.board.board[self.board.board < 1] = 0
        self.hits = np.zeros((gamedef.rows, gamedef.cols))
        self.misses = np.zeros((gamedef.rows, gamedef.cols))
        self.moves = 0

    def to_str(self):
        def stringify_cell(hit, miss):
            if hit == 0 and miss == 0:
                return '*'
            elif hit == 1:
                return 'X'
            elif miss == 1:
                return '.'

        s = ''
        for y in range(self.gamedef.rows):
            for x in range(self.gamedef.cols):
                s += stringify_cell(self.hits[y, x], self.misses[y, x])
        return s

    def fire(self, y, x):
        self.moves += 1
        if self.board.board[y, x] == 1:
            self.hits[y, x] = 1
        else:
            self.misses[y, x] = 1

        grid = self.to_str()
        cell = grid[y*self.gamedef.rows + x]
        result = True
        avenger = False
        map_id = 0
        map_count = 1
        move_count = self.moves
        is_finished = self.finished()

        return FireResponse(grid=grid, cell=cell,
                            result=result, avengerAvailable=avenger,
                            mapId=map_id, mapCount=map_count,
                            moveCount=move_count,
                            finished=is_finished)

    # def ask(self, y, x):
    #     if self.board.board[y, x] == 1:
    #         self.hits[y, x] = 1
    #         return True
    #     return False

    def finished(self):
        return np.array_equal(self.board.board, self.hits)

    def print_board(self):
        self.board.print()
