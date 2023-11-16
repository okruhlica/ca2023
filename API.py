def empty_fire_response(rows, cols):
    grid = '*' * (rows * cols)
    return FireResponse(grid, '', False)


class FireResponse:
    def __init__(self, grid, cell, result, avengerAvailable=False, mapId=0, mapCount=1, moveCount=0, finished=False):
        self.grid = grid
        self.cell = cell
        self.result = result
        self.avenger_available = avengerAvailable
        self.map_id = mapId
        self.map_count = mapCount
        self.move_count = moveCount
        self.game_finished = finished
