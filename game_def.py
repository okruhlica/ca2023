from fleet import Fleet


class GameDef:
    def __init__(self, rows, cols, ships):
        self.rows = rows
        self.cols = cols
        self.fleet = Fleet()
        self.fleet.from_list(ships)


_CA23_GAME_SHIPS = [
    {'name': 'Patrol Boat',
     'variants': ['11', '1|1'],
     'size': 2,
     'part_of': ['Submarine', 'Cruiser', 'Battleship', 'Carrier', 'Avengers Helicarrier'],
     'priority': 5
     },
    {'name': 'Submarine',
     'variants': ['111', '1|1|1'],
     'size': 3,
     'part_of': ['Battleship', 'Carrier', 'Avengers Helicarrier'],
     'priority': 4
     },
    {'name': 'Destroyer',
     'variants': ['111', '1|1|1'],
     'size': 3,
     'priority': 3
     },
    {'name': 'Battleship',
     'variants': ['1111', '1|1|1|1'],
     'size': 4,
     'part_of': ['Carrier', 'Avengers Helicarrier'],
     'priority': 2
     },
    {'name': 'Carrier',
     'variants': ['11111', '1|1|1|1|1'],
     'size': 5,
     'part_of': ['Avengers Helicarrier'],
     'priority': 1
     },
    {'name': 'Avengers Helicarrier',
     'variants': ['01010|11111|01010', '010|111|010|111|010'],
     'size': 9,
     'part_of': [],
     'priority': 0
     },
]

CA2023_GAME_DEF = GameDef(rows=12, cols=12, ships=_CA23_GAME_SHIPS)
