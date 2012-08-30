import unittest

from backgammon import *

class TestGame(unittest.TestCase) :
    def setup(self) :
        pass

    def assertOfType(self, obj, expected_type) :
        self.failIf(type(obj) !=  expected_type,
            "Expecting object of type " + str(expected_type) 
            + " got object of type " + str(type(obj)))

    def testMove(self) :
        # test moving on top of other player (should get err)
        self.assertOfType(Game(dice = [5]).move([(0,5)]), str)

################################################################################

if __name__ == '__main__' :
    unittest.main()
