import numpy as np

import ai_v1
import ai_v2
from boards import generate_random_board


class Captain:
    def __init__(self):
        self.board = generate_random_board(12, 12)
        self.board.board[self.board.board < 1] = 0
        self.hits = np.zeros((12, 12))

    def ask(self, y, x):
        if self.board.board[y, x] == 1:
            self.hits[y, x] = 1
            return True
        return False

    def finished(self):
        return np.array_equal(self.board.board, self.hits)

    def print_board(self):
        self.board.print()


def play_random_games(opponent, count=40):
    sum_turns = 0.0
    for game in range(count):
        turns = 0
        p0 = Captain()
        p1 = opponent(p0.ask)

        while not p0.finished():
            # print(f"Turn #{turns}")
            turns += 1.0
            if not p1.move():
                break

        if p1.hits != 9:
            print(f"!ASSERTION ERROR! ({p1.hits}/9 hits)")
            print("Game:")
            p0.print_board()
            print("Guessboard:")
            p1.print_board()
            return
        sum_turns += turns
    return sum_turns / count


if __name__ == '__main__':
    # while True:
    avg_dummy = play_random_games(ai_v1.RandomGuesser, 1000)
    print(f"Average turns ({ai_v1.RandomGuesser.NAME}): {avg_dummy}")

    avg_stat = play_random_games(ai_v2.StatisticalGuesser, 1000)
    print(f"Average turns ({ai_v2.StatisticalGuesser.NAME}): {avg_stat}")
