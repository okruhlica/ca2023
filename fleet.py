from ship import Ship, ShipShapeType


class Fleet:
    def __init__(self):
        self.ships = []

    def from_list(self, obj, row_delim='|', char_ship='1'):
        def parse_ship_definition(o):
            variants = []
            for variant in o['variants']:
                shipobj = Ship(ship['name'])
                shipobj.from_str(variant, row_delim=row_delim, char_ship=char_ship)
                variants.append(shipobj)

            return {
                'name': variants[0].name,
                'size': variants[0].pieces(),
                'variants': variants
            }

        for ship in obj:
            self.ships.append(parse_ship_definition(ship))

    def hits_needed(self):
        return sum([ship['size'] for ship in self.ships])