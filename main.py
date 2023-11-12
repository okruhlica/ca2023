import ai_v1
import ai_v2
import game
from game import play_random_games

if __name__ == '__main__':
    from game_def import CA2023_GAME_DEF
    game_engine = game.GameEngine
    avg_dummy = play_random_games(game_engine, ai_v1.RandomGuesser, CA2023_GAME_DEF, iterations=100)
    print(f"Average turns ({ai_v1.RandomGuesser.NAME}): {avg_dummy}")

    avg_stat = play_random_games(game_engine, ai_v2.StatisticalGuesser, CA2023_GAME_DEF, iterations=100)
    print(f"Average turns ({ai_v2.StatisticalGuesser.NAME}): {avg_stat}")
