import enum

import numpy as np


class ShipShapeType(enum.Enum):
    SHIP_TRIMMED = 0
    SHIP_PLUS_ONE = 1
    BUFFER_ONLY = 2
    SHIP_AND_BUFFER = 3


class Ship:
    def __init__(self, name):
        self.name = name
        self.ship = None
        self.ship_height, self.ship_width = None, None

        self.buffer_mask = None
        self.combined_mask = None

    def generate_buffer_mask(self, base_shape):
        h, w = base_shape.shape
        mask = np.zeros((h, w))

        for y in range(1,h-1):
            for x in range(1,w-1):
                if base_shape[y, x] == 1:
                    for xx in range(max(0, x - 1), min(x + 2, w + 1)):
                        for yy in range(max(0, y - 1), min(y + 2, h + 1)):
                            if base_shape[yy, xx] == 0:
                                mask[yy, xx] = 1
        return mask

    def from_str(self, s, row_delim='|', char_ship='1'):
        lines = s.split(row_delim)
        assert all([len(l) == len(lines[0]) for l in lines])

        rows, cols = len(lines), len(lines[0])
        mx = np.zeros((rows, cols), dtype=float)

        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == char_ship:
                    mx[y, x] = 1

        self.set_shape(mx)

    def set_shape(self, ship_shape):
        '''
        Sets the ship's shape and all internal variants of (buffer, masks, etc.)
        Assumption: ship_shape is a 2D numpy array without buffers.
        '''
        # Pad the ship from all sides with by one
        if len(ship_shape.shape) == 1:
            self.ship_height, self.ship_width = 1, ship_shape.shape[0]
        else:
            self.ship_height, self.ship_width = ship_shape.shape

        self.ship = np.zeros((self.ship_height + 2, self.ship_width + 2))
        self.ship[1:-1, 1:-1] = ship_shape

        # Calculate the masks
        self.buffer_mask = self.generate_buffer_mask(self.ship)
        self.combined_mask = np.add(self.ship, self.buffer_mask)

    def get_shape(self, kind=ShipShapeType.SHIP_TRIMMED):
        if kind == ShipShapeType.SHIP_TRIMMED:
            return self.ship[1:-1, 1:-1]
        elif kind == ShipShapeType.SHIP_PLUS_ONE:
            return self.ship
        elif kind == ShipShapeType.SHIP_AND_BUFFER:
            return self.combined_mask
        elif kind == ShipShapeType.BUFFER_ONLY:
            return self.buffer_mask
        return None

    def pieces(self):
        return self.ship.sum()

    def __eq__(self, other):
        this = self.get_shape(kind=ShipShapeType.SHIP_TRIMMED)
        other = other.get_shape(kind=ShipShapeType.SHIP_TRIMMED)
        return np.array_equal(this, other)
