from unittest import TestCase

from fleet import Fleet


class TestFleet(TestCase):
    def setUp(self) -> None:
        FLEET = [{'name': 'Destroyer',
                  'variants': ['11', '1|1'],
                  },
                 {'name': 'Submarine',
                  'variants': ['111', '1|1|1'],

                  }]
        self.flotilla = Fleet()
        self.flotilla.from_list(FLEET)

    def test_from_list(self):

        self.assertEqual(self.flotilla.ships[0]['name'], 'Destroyer')
        self.assertEqual(self.flotilla.ships[1]['name'], 'Submarine')

        for ship in self.flotilla.ships:
            for var in ship['variants']:
                self.assertEqual(var.pieces(), ship['variants'][0].pieces())
                self.assertEqual(var.pieces(), ship['size'])

    def test_hits_needed(self):
        self.assertEqual(self.flotilla.hits_needed(), 5)