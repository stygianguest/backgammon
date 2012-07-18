from random import randint

BOARD_LENGTH = 4 * 6
NO_DICE = 2
DICE_SIZE = 6

class Game :
    def __init__(self, other = None) :
        if other != None :
            # copy the state of the other game
            self.board = list(other.board)
            self.player = other.player
            self.dice = list(other.dice)
            self.side = list(other.side)
            return
            
        self.board = [ 0 for i in range(BOARD_LENGTH) ]

        # negative token is black, positive white
        for i in [0]*2 + [11]*5 + [16]*3 + [18]*5 :
            self.board[i] += 1
            self.board[-i-1] += -1

        # self.tokens[player] are the number of off-game tokens of player {1,-1}
        # since this isn't shared token count is always positive
        self.side = [0,0]

        # players 1 and -1 (used for step direction)
        self.player = -1
        self.throw()

    def throw(self) :
        self.player = -self.player
        self.dice = [ randint(1,DICE_SIZE) for i in range(NO_DICE) ]

        if all((self.dice[0] == i for i in self.dice )) :
            # if the dice are the same, double the dice
            self.dice = self.dice * 2

    def move(self, actions) :
        # the pairs (t,s) in actions are commands that move the token at t s
        # steps where the direction depends on the current player offside
        # tokens have position -1

        if len(filter(lambda (t,s) : t == -1, actions)) < min(len(self.dice), 
                self.side[self.player]) :
            return "Must move as many tokens as possible from the side first"

        if not isSubBag([s for t,s in actions], self.dice) :
            return "Moves are inconsistent with the dice"

        # the new game state to be
        after = Game(self)

        # execute the actions
        for (o,s) in actions :
            d = o + (s*self.player)
            if after.board[o]*self.player <= 0 :
                return "Can only move current player's tokens"

            if self.player * (after.board[d] + self.player) < 0 :
                return "Can only move on top of at most one token of the other player"

            after.board[o] -= after.player
            after.dice.remove(s)

            if d >= BOARD_LENGTH :
                # if token is moved off the board, remove it from the game
                # that means, don't add it anywhere
                continue

            if after.board[d] * after.player == 1 :
                # stepping on top of someone: remove the token
                after.board[d] = 0
                after.side[-after.player] += 1

            after.board[d] += after.player
        
        ## check if all dice are utilized
        ## try all tokens and see if they could move
        #for s in after.moves :
        #    for o in range(BOARD_LENGTH) :
        #        d = o + (s*self.player)
        #        # if current player has a token at position o
        #        if after.board[o] * after.player <= 0 :
        #            # and the other player has no more than a single token
        #            # at the destinatoin
        #            if after.board[d] * after.player > 1 :

        # prepare for the next move
        after.throw()
        
        return after

    def __str__(self) :
        s = str(self.side[-1]) + " "
        if self.player == -1 :
            s += str(self.dice)
        s += "\n"
        s += concat(intersperse(map(str, self.board[6:12][::-1]), " "))
        s += "\t"
        s += concat(intersperse(map(str, self.board[0:6][::-1]), " "))
        s += "\n"
        s += concat(intersperse(map(str, self.board[12:18]), " "))
        s += "\t"
        s += concat(intersperse(map(str, self.board[18:24]), " "))
        s += "\n"
        s += str(self.side[1]) + " "
        if self.player == 1 :
            s += str(self.dice)

        return s


def concat(lsts) :
    if type(lsts[0]) is str :
        return reduce(str.__add__, lsts)

    return [ i for lst in lsts for i in lst ]

def intersperse(lst, sep) :
    if not list :
        return lst
    return concat([ (i,sep) for i in lst[:-1] ]) + [lst[-1]]

################################################################################

def isSubBag(x, y) :
    x = list(x)
    y = list(y)

    while x :
        try :
            y.remove(x.pop())
        except ValueError:
            return False

    return True

assert isSubBag([],[])
assert isSubBag([1],[1])
assert isSubBag([1,2],[1,2])
assert isSubBag([1,1,2],[1,1,2])
assert isSubBag([1,2,1],[1,2,1])
assert isSubBag([],[1])
assert isSubBag([1],[1,2])
assert isSubBag([1,2],[1,1,2])
assert isSubBag([1,2],[1,2,1])

assert not isSubBag([1],[])
assert not isSubBag([1],[2])
assert not isSubBag([1,2],[1])
assert not isSubBag([1,2,1],[1,2])

################################################################################

g = Game()
print g
print g.move(zip([0,0], g.dice))

