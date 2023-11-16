from unittest import TestCase

import numpy as np

from boards import ZeroOneBoard


class Test(TestCase):
    def test__get_shape_2d(self):
        from boards import _get_shape_2d

        obj1D = np.zeros((3))
        self.assertEqual((1, 3), _get_shape_2d(obj1D))

        obj2D = np.zeros((2, 4))
        self.assertEqual((2, 4), _get_shape_2d(obj2D))

        obj3D = np.zeros((2, 4, 6))
        self.assertEqual((2, 4), _get_shape_2d(obj3D))

        obj0D = np.zeros((0))
        self.assertEqual((0, 0), _get_shape_2d(obj0D))

def make_shape(rows, cols, fill=0):
    mx = np.zeros((rows, cols))
    if fill != 0:
        mx[:,:] = fill
    return mx

def make_shape1D(cols, fill=0):
    mx = np.zeros((cols))
    if fill != 0:
        mx[:] = fill
    return mx

class TestBooleanBoard(TestCase):
    def test_fits(self):

        board = ZeroOneBoard(12, 12)
        self.assertTrue(board.fits(0, 0, make_shape(12, 12)))
        self.assertTrue(board.fits(1, 1, make_shape(11, 11)))
        self.assertTrue(board.fits(10, 10, make_shape(2, 2)))
        self.assertTrue(board.fits(11, 0, make_shape(1, 11)))
        self.assertTrue(board.fits(0, 11, make_shape(11, 1)))

        self.assertTrue(board.fits(0, 0, make_shape1D(1)))
        self.assertTrue(board.fits(10, 0, make_shape1D(2)))

        self.assertFalse(board.fits(-1, -1, make_shape(1, 1)))
        self.assertFalse(board.fits(-1, -1, make_shape(2, 2)))
        self.assertFalse(board.fits(-1, -1, make_shape1D(2)))

        self.assertFalse(board.fits(11, 0, make_shape(2, 1)))
        self.assertFalse(board.fits(10, 11, make_shape(1, 2)))
        self.assertFalse(board.fits(0, 0, make_shape(13, 13)))

    def test_place(self):
        board = ZeroOneBoard(12, 12)
        self.assertEqual(0, board.board.sum())

        s0 = make_shape1D(1)
        board.place(0,0,s0)
        self.assertEqual(0, board.board.sum())

        s1 = make_shape1D(3)
        s1[0] = 1
        board.place(0,0,s1)
        self.assertEqual(1, board.board.sum())

        board.place(0, 0, s1)
        self.assertEqual(1, board.board.sum())

        board.place(1, 0, s1)
        self.assertEqual(2, board.board.sum())

        s2 = make_shape(12,12)
        s2[:,:] = 1
        board.place(0,0,s2)
        self.assertEqual(12*12, board.board.sum())

        board.reset()
        self.assertEqual(0, board.board.sum())

    def test_can_place(self):
        board = ZeroOneBoard(12, 12)
        s = make_shape1D(1, fill=1)
        board.place(0,0, s)
        self.assertFalse(board.can_place(0,0,s))
        self.assertTrue(board.can_place(0,1,s))
        self.assertTrue(board.can_place(1, 0, s))
        self.assertTrue(board.can_place(1, 1, s))
        self.assertTrue(board.can_place(10, 10, s))


        board.reset()


