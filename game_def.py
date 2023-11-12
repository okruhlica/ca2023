from utils import parse_ship


class GameDef:
    def __init__(self, rows, cols, ships):
        self.rows = rows
        self.cols = cols
        self.fleet = ships
        self.hits_needed = sum([(ship['shapes'][0]==1).sum() for ship in ships])


_CA23_GAME_SHIPS = [
    {'name': 'Destroyer',
     'shapes': parse_ship(['11', '1|1'])
     },
    {'name': 'Submarine',
     'shapes': parse_ship(['111', '1|1|1'])
     },
    {'name': 'Cruiser',
     'shapes': parse_ship(['111', '1|1|1'])
     },
    {'name': 'Battleship',
     'shapes': parse_ship(['1111', '1|1|1|1'])
     },
    {'name': 'Carrier',
     'shapes': parse_ship(['11111', '1|1|1|1|1'])
     },
    {'name': 'Avengers Helicarrier',
     'shapes': parse_ship(['01010|11111|01010', '010|111|010|111|010'])
     },
]

CA2023_GAME_DEF = GameDef(rows=12, cols=12, ships=_CA23_GAME_SHIPS)
