import os
from random import choice, shuffle

import ai_v1
import game_def
from boards import ZeroOneBoard
from opponent import MockOpponent
def play_random_games(engine, opponent, gamedef, iterations=20):
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
    return sum_turns #/ iterations

def load_local_board(path, id):
    uri = os.path.join(path, str(id)+'.board')
    board = ZeroOneBoard(0,0)
    board.from_str(open(uri, 'r').read().strip())
    return board

def play_game(op, bot):
    turns = 0.
    while not op.finished():
        turns += 1.
        if not bot.move():
            print('Bot has given up :(')
            turns = 10000000
            break

    # if p1.hits != gamedef.hits_needed:
    #     print(f"!ASSERTION ERROR! ({p1.hits}/9 hits)")
    #     print("Game:")
    #     p0.print_board()
    #     print("Guessboard:")
    #     p1.print_board()
    #     return
    return turns


if __name__ == '__main__':
    iterations = 20
    gamedef = game_def.CA2023_GAME_DEF
    bot_cls = ai_v1.RandomGuesser

    ids = [i for i in range(100)]
    shuffle(ids)
    boards = [load_local_board('data/boards/', num) for num in ids]

    total_turns = 0.
    for it in range(iterations):
        opponent = MockOpponent(boards[it])
        bot = bot_cls(opponent.fire_at, gamedef)
        total_turns+= play_game(opponent, bot)

    print(f"{iterations} games played, average score was {total_turns/iterations}")
