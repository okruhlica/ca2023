from unittest import TestCase

import numpy as np

from ship import Ship, ShipShapeType


class TestShip(TestCase):

    def test_from_str(self):
        ship1 = Ship('corvette')

        shipstr = '1'
        ship1.from_str(shipstr)
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_AND_BUFFER).shape, (3, 3))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_TRIMMED).shape, (1, 1))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.BUFFER_ONLY).shape, (3, 3))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_PLUS_ONE).shape, (3, 3))

        shipstr = '1111'
        ship1.from_str(shipstr)
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_AND_BUFFER).shape, (3, 6))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_TRIMMED).shape, (1, 4))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.BUFFER_ONLY).shape, (3, 6))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_PLUS_ONE).shape, (3, 6))

        shipstr = '11|01'
        ship1.from_str(shipstr)
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_AND_BUFFER).shape, (4, 4))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_TRIMMED).shape, (2, 2))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.BUFFER_ONLY).shape, (4, 4))
        self.assertEqual(ship1.get_shape(kind=ShipShapeType.SHIP_PLUS_ONE).shape, (4, 4))

    def test_pieces(self):
        ship1 = Ship('?')
        shipstr = '11|01'
        ship1.from_str(shipstr)
        self.assertEqual(3, ship1.pieces())

    def test_eq(self):
        ship1 = Ship('?')
        ship1.from_str('11|01')

        ship2 = Ship('!')
        ship2.set_shape(np.array([[1, 1], [0, 1]]))

        self.assertTrue(ship1 == ship2)
        self.assertTrue(ship2 == ship1)
        self.assertTrue(ship2 == ship2)
        self.assertTrue(ship1 == ship1)

        ship1.from_str('1')
        self.assertFalse(ship1 == ship2)
        ship2.from_str('1')
        self.assertTrue(ship1 == ship2)

    def test_set_shape(self):
        ship = Ship('one')

        # Test 1: Ship "1"
        ship.set_shape(np.array([1]))

        trimmed = ship.get_shape(kind=ShipShapeType.SHIP_TRIMMED)
        self.assertTrue(np.array_equal(trimmed, np.array([[1.]])))

        plus1 = ship.get_shape(kind=ShipShapeType.SHIP_PLUS_ONE)
        self.assertTrue(np.array_equal(plus1, np.array([[0, 0, 0], [0, 1., 0], [0, 0, 0]])))

        buff = ship.get_shape(kind=ShipShapeType.BUFFER_ONLY)
        self.assertTrue(np.array_equal(buff, np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])))

        shipandbuff = ship.get_shape(kind=ShipShapeType.SHIP_AND_BUFFER)
        self.assertTrue(np.array_equal(shipandbuff, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])))

        # Test 2: Ship "1|1"
        ship.from_str('1|1')
        trimmed = ship.get_shape(kind=ShipShapeType.SHIP_TRIMMED)
        self.assertTrue(np.array_equal(trimmed, np.array([[1.], [1.]])))

        plus1 = ship.get_shape(kind=ShipShapeType.SHIP_PLUS_ONE)
        self.assertTrue(np.array_equal(plus1, np.array([[0, 0, 0], [0, 1., 0], [0, 1, 0], [0, 0, 0]])))

        buff = ship.get_shape(kind=ShipShapeType.BUFFER_ONLY)
        self.assertTrue(np.array_equal(buff, np.array([[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]])))

        shipandbuff = ship.get_shape(kind=ShipShapeType.SHIP_AND_BUFFER)
        self.assertTrue(np.array_equal(shipandbuff, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])))
