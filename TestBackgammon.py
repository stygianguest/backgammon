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
        #TODO: test actual error types? then I should raise custom exceptions

        # ignoring tokens from the side
        self.assertOfType(
            Game(side = {1 : 0, -1 : 2}, dice = [2]).move([(23,2)]), str)

        # steps inconsistent with dice
        self.assertOfType(Game(dice = [1]).move([(23,2)]), str)

        # move from empty place
        self.assertOfType(Game(dice = [1]).move([(22,1)]), str)

        # move other player's token
        self.assertOfType(Game(dice = [1]).move([(18,1)]), str)

        # test moving on top of other player (should get err)
        self.assertOfType(Game(dice = [5]).move([(23,5)]), str)

    def testMove(self) :
        # simple, legal move, into void of single token
        self.assertEquals(Game(dice = [1], board = [0]).move([(23,1)]).board,
            [1] + [0]*21 + [-1,0])

        # moving on top of other token (owned by same player)
        self.assertEquals(Game(dice = [1], board = [0,1]).move([(23,1)]).board,
            [1,1] + [0]*20 + [-2,0])

        # moving two tokens
        self.assertEquals(
            Game(dice = [1,1], board = [0,1]).move([(22,1),(23,1)]).board,
            [1,1] + [0]*19 + [-1,-1,0])

        # moving the same token twice
        self.assertEquals(
            Game(dice = [1,1], board = [0]).move([(23,1), (22,1)]).board,
            [1] + [0]*20 + [-1,0,0])

        # hitting the opponent's token
        self.assertEquals(
            Game(dice = [1], board = [0,22]).move([(23,1)]).board,
            [1,-1] + [0]*20 + [-1,0])
        self.assertEquals(
            Game(dice = [1], board = [0,22]).move([(23,1)]).side,
            {1 : 1, -1 : 0})

        # hitting the opponent's token and moving on
        self.assertEquals(
            Game(dice = [1,1], board = [0,22]).move([(23,1), (22,1)]).board,
            [1,-1] + [0]*19 + [-1,0,0])
        self.assertEquals(
            Game(dice = [1], board = [0,22]).move([(23,1)]).side,
            {1 : 1, -1 : 0})
        

################################################################################

if __name__ == '__main__' :
    unittest.main()
