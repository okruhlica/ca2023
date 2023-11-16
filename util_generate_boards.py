import os.path
import random
from random import randint, choice

from boards import ZeroOneBoard
from fleet import Fleet
from game_def import CA2023_GAME_DEF
from ship import ShipShapeType


def generate_random_board(gamedef):
    b = ZeroOneBoard(gamedef.rows, gamedef.cols)
    # regenerate = False
    fleet = Fleet()
    fleet.from_list(gamedef.fleet)
    random.shuffle(fleet.ships)

    regenerate = False
    for ship_type in fleet.ships:
        count = 1
        its = 0
        while count > 0:
            its += 1
            rx, ry = randint(0, b.cols - 1), randint(0, b.rows - 1)
            ship = choice(ship_type['variants'])
            if b.can_place(ry, rx, ship.get_shape(ShipShapeType.SHIP_AND_BUFFER)):
                b.place(ry, rx, ship.get_shape(ShipShapeType.SHIP_PLUS_ONE))
                count -= 1
            if its > gamedef.cols * gamedef.rows:
                regenerate = True
                break
        if regenerate:
            break
    if regenerate:
        return generate_random_board(gamedef)
    return b


if __name__ == '__main__':
    samples = 100
    fs_path = 'data/boards/'

    for iteration in range(samples):
        board = generate_random_board(CA2023_GAME_DEF)
        with open(os.path.join(fs_path, str(iteration) + '.board'), "w") as text_file:
            text_file.write(str(board))
