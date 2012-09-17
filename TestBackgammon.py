import unittest

from backgammon import *

class TestGame(unittest.TestCase) :
    def setup(self) :
        pass

    def assertOfType(self, obj, expected_type) :
        self.failIf(type(obj) !=  expected_type,
            "Expecting object of type " + str(expected_type) 
            + " got object of type " + str(type(obj)))

    def testMoveErrors(self) :
        # ignoring tokens from the bar
        self.assertRaises(Exception,
            Game(bar = {1 : 0, -1 : 2}, dice = [2]).move, 23,2)

        # steps inconsistent with dice
        self.assertRaises(Exception, Game(dice = [1]).move, 23, 2)

        # move from empty place
        self.assertRaises(Exception, Game(dice = [1]).move, 22, 1)

        # move other player's token
        self.assertRaises(Exception, Game(dice = [1]).move, 18, 1)

        # test moving on top of other player (should get err)
        self.assertRaises(Exception, Game(dice = [5]).move, 23, 5)


    def testMove(self) :
        # simple, legal move, into void of single token
        self.assertEquals(Game(dice = [1], board = [0]).move(23, 1).board,
            [1] + [0]*21 + [-1,0])

        # moving on top of other token (owned by same player)
        self.assertEquals(Game(dice = [1], board = [0,1]).move(23, 1).board,
            [1,1] + [0]*20 + [-2,0])

        # moving two tokens
        #self.assertEquals(
        #    Game(dice = [1,1], board = [0,1]).move([(22,1),(23,1)]).board,
        #    [1,1] + [0]*19 + [-1,-1,0])

        # moving the same token twice
        #self.assertEquals(
        #    Game(dice = [1,1], board = [0]).move([(23,1), (22,1)]).board,
        #    [1] + [0]*20 + [-1,0,0])

        # hitting the opponent's token
        self.assertEquals(
            Game(dice = [1], board = [0,22]).move(23,1).board,
            [1,-1] + [0]*20 + [-1,0])
        self.assertEquals(
            Game(dice = [1], board = [0,22]).move(23,1).bar,
            {1 : 1, -1 : 0})

        # hitting the opponent's token and moving on
        #self.assertEquals(
        #    Game(dice = [1,1], board = [0,22]).move([(23,1), (22,1)]).board,
        #    [1,-1] + [0]*19 + [-1,0,0])
        #self.assertEquals(
        #    Game(dice = [1], board = [0,22]).move([(23,1)]).bar,
        #    {1 : 1, -1 : 0})

        # moving from the bar
        self.assertEquals(
            Game(dice = [1], board = [], bar = {1 : 0, -1 : 1}).move(-1,1).board,
            [0]*23 + [-1])
        self.assertEquals(
            Game(dice = [1], board = [], bar = {1 : 0, -1 : 1}).move(-1,1).bar,
            {1 : 0, -1 : 0})

    def testCanMove(self) :
        # no more legal moves with token blocked on the bar
        self.assertFalse(
            Game(dice = [1], board = [23,23], bar = {1 : 0, -1 : 1}).canMove())

        # no more legal moves left with the current dice (blocked)
        self.assertFalse(
            Game(dice = [1], board = [0,0,22,22]).canMove())

        # no more tokens left
        self.assertFalse(
            Game(dice = [1], board = []).canMove())

        # still legal moves possible, simple unused dice
        self.assertTrue(Game(dice = [1]).canMove())
        
        # still legal moves possible from the bar
        self.assertTrue(
            Game(dice = [1], board = [], bar = {1 : 0, -1 : 1}).canMove())

        # can still do collecting move
        self.assertTrue(Game(dice = [3], board=[23]).canMove())
        

################################################################################

if __name__ == '__main__' :
    unittest.main()
