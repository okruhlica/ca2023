import numpy as np
from numpy import uint8


def parse(lst):
    def parse_one(s):
        lines = s.split('|')
        assert all([len(l) == len(lines[0]) for l in lines])

        sy, sx = len(lines) + 2, len(lines[0]) + 2
        mx = np.zeros((sy, sx), dtype=float)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '1':
                    mx[y + 1, x + 1] = 1

        # Set neighboring indicators
        for y in range(sy):
            for x in range(sx):
                if mx[y, x] == 1:
                    for xx in range(max(0, x - 1), min(x + 2, sx + 1)):
                        for yy in range(max(0, y - 1), min(y + 2, sy + 1)):
                            mx[yy, xx] = 0.5 if mx[yy, xx] < 1 else 1
        return mx

    out = []
    for ship in lst:
        out.append(parse_one(ship))
    return out


SHIPS = [
    {'name': 'small',
     'shapes': parse(['11', '1|1'])
     },
    {'name': 'mid',
     'shapes': parse(['111', '1|1|1'])
     },
    {'name': 'big',
     'shapes': parse(['111|010', '010|111', '10|11|10', '01|11|01'])
     }
]

SHIP_COUNTS = {'small': 1, 'mid': 1, 'big': 1}
