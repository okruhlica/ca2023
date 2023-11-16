import os
import time
from random import choice, shuffle

import ai_v1
import ai_v2
import game_def
from boards import ZeroOneBoard
from opponent import MockOpponent


def load_local_board(path, id):
    uri = os.path.join(path, str(id) + '.board')
    board = ZeroOneBoard(0, 0)
    board.from_str(open(uri, 'r').read().strip())
    return board


def play_games(maps, bot_cls, count):
    total_turns = 0.
    start = time.time()

    for it in range(count):
        opponent = MockOpponent(maps[it].copy())
        assert (maps[it].ones() == 26)
        bot = bot_cls(opponent.fire_at, gamedef)
        total_turns += play_single_game(opponent, bot)

    end = time.time()
    duration = round((end - start) * 1000)

    print(
        f"{bot_cls.__name__} player {iterations} games and needed {total_turns / iterations} turns on average to finish a game. That's a score of approx. {round(200*(total_turns / iterations))} pts.")
    print(f"Games took {duration}ms ({duration / iterations}ms on average per game)\n")


def play_single_game(op, bot):
    turns = 0.
    while not op.finished():
        turns += 1.
        if not bot.move():
            print('Bot has given up :(')
            turns = 10000000
            break
    return turns


if __name__ == '__main__':
    iterations = 100
    gamedef = game_def.CA2023_GAME_DEF
    bots = [ai_v1.RandomGuesser, ai_v2.StatisticalGuesser]

    # Init maps
    MAPS_AVAILABLE = 500
    map_ids = [i for i in range(MAPS_AVAILABLE)]
    # shuffle(map_ids)
    selected_maps = [load_local_board('data/boards/', num) for num in map_ids]

    for bot in bots:
        play_games(selected_maps.copy(), bot, iterations)
