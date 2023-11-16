from pprint import pprint

import numpy as np

import game_def
from boards import StatsBoard, Board

HIT = 1
MISS = -1
UNKNOWN = 0


def construct_mask_for(hitboard, h, w):
    if hitboard.ship[0] < h or hitboard.ship[1] < w:
        return None

    mask = hitboard[:h, :w].copy()
    mask[mask != HIT] = 0
    return mask

def match_shape_hits(hitboard, shape):
        sh_w, sh_h = shape.ship[1], shape.ship[0]

        marked = np.zeros((hitboard.rows, hitboard.cols))
        for y in range(hitboard.rows - sh_h):
            for x in range(hitboard.cols - sh_w):
                mask = construct_mask_for(hitboard.board[y:, x:], sh_h, sh_w)
                if mask.sum() == 0:
                    continue  # No hits in this area? Move on.

                if hitboard.can_place(y, x, shape, check_proximity=False, fit_mask=mask):
                    marked[y:y+mask.shape[0], x:x+mask.shape[1]] += mask
        return marked


def identify_ships(board, fleet):

    mx = board.board.copy()

    ships = sorted(fleet, key=lambda x: x['_order'])
    pprint(ships)

    sunk, unsunk = [], []
    ship_id = 0
    #
    # for ship in ships:
    #     name = ship['name']
    #     for shape in ship['shapes']:
    #         positions = find_sure_shape(shape)


if __name__ == '__main__':
    # identify_ships(None, game_def.CA2023_GAME_DEF.fleet)
    hboard = Board(12, 12)
    # hboard.board[0, 0] = HIT
    hboard.board[0, 0] = HIT
    hboard.board[0, 2] = MISS
    # pprint(construct_mask_for(hboard, 2, 2))
    destroyer = game_def.CA2023_GAME_DEF.fleet[0]['shapes'][0]
    pprint(match_shape_hits(hitboard=hboard, shape=destroyer))