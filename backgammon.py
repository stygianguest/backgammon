from random import randint

BOARD_LENGTH = 4 * 6
NO_DICE = 2
DICE_SIZE = 6

class Game :
    def __init__(self, other = None, dice = None, player = -1, 
        bar = {1 : 0, -1 : 0},
        board=([0]*2 + [11]*5 + [16]*3 + [18]*5)) :

        if other :
            # copy the state of the other game
            self.board = list(other.board)
            self.player = other.player
            self.dice = list(other.dice)
            self.bar = dict(other.bar)
            return
            
        self.board = [ 0 for i in range(BOARD_LENGTH) ]

        # negative checker is black, positive white
        for i in board :
            self.board[i] += 1
            self.board[-i-1] += -1

        # since this isn't shared checker count is always positive
        self.bar = bar

        # players 1 and -1 (used for step direction)
        self.player = player

        if dice :
            self.dice = dice
        else :
            self.throw()

    def throw(self) :
        self.player = -self.player
        self.dice = [ randint(1,DICE_SIZE) for i in range(NO_DICE) ]

        if all((self.dice[0] == i for i in self.dice )) :
            # if the dice are the same, double the dice
            self.dice = self.dice * 2

    def move(self, o, s) :
        # move the checker at origin to destination (o+s) in a new game object
        # the bar has position -1 as origin when entering a checker 
        # collecting a checker is done by moving past the end of the board

        if self.bar[self.player] > 0 and o != -1 :
            raise Exception("Must move as many checkers as possible from the bar first")

        if s not in self.dice :
            raise Exception("No die matching the move")

        if o != -1 and self.board[o]*self.player <= 0 :
            raise Exception("Must move checker owned by this player")

        if o == -1 and self.bar[self.player] <= 0 :
            raise Exception("There is no checker on the bar")

        # adjust in case we're coming from the bar (-1 or 24 dep on player)
        d = (24 if self.player == o else o) + s*self.player

        if self.player * (self.board[d] + self.player) < 0 :
            raise Exception("Can only move on top of at most one checker of the other player")

        # the new game state to be
        after = Game(self)

        if o == -1 :
            after.bar[after.player] -= 1
        else :
            after.board[o] -= after.player

        after.dice.remove(s)

        if d >= BOARD_LENGTH or d < 0 :
            # if checker is moved off the board, remove it from the game
            # that means, don't add it anywhere
            return after

        if after.board[d] == -after.player :
            # stepping on top of someone: remove the checker
            after.board[d] = 0
            after.bar[-after.player] += 1

        after.board[d] += after.player

        return after

    def __repr__(self) :
        return str(self)

    def __str__(self) :
        s = str(self.bar[-1]) + " "
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
        s += str(self.bar[1]) + " "
        if self.player == 1 :
            s += str(self.dice)

        return s

    def winner(self) :
        if sum((p if p<0 else 0 for p in self.board), self.bar[-1]) == 0 :
            return -1

        if sum((p if p>0 else 0 for p in self.board), self.bar[1]) == 0 :
            return 1

        return None

    def isOver(self) :
        return bool(self.winner())

    def nexts(self) :
        last = []
        current = [self]

        while current != [] :
            last = current
            current = []

            # to advance a step from the current games
            for game in last :
                # try all dice
                for s in game.dice :
                    # if there's checkers on the bar, try those
                    if game.bar[game.player] > 0 :
                        try : current.append(game.move(-1,s))
                        except Exception : pass
                    else : # otherwise try to move the checkers on the board
                        for o in range(BOARD_LENGTH) :
                            try : current.append(game.move(o,s))
                            except Exception : pass

        return last


    def canMove(self) :
        #FIXME: code duplication? in Game.nexts
        for s in self.dice :
            if self.bar[self.player] > 0 :
                try :
                    self.move(-1,s)
                    return True
                except Exception :
                    pass
            else :
                for o in range(BOARD_LENGTH) :
                    try :
                        self.move(o,s)
                        return True
                    except Exception :
                        pass
        return False


def concat(lsts) :
    if type(lsts[0]) is str :
        return reduce(str.__add__, lsts)

    return [ i for lst in lsts for i in lst ]

def intersperse(lst, sep) :
    if not list :
        return lst
    return concat([ (i,sep) for i in lst[:-1] ]) + [lst[-1]]

################################################################################

if __name__ == '__main__' :
    game = Game()

    # loop until the game is over
    while not game.isOver() :

        turn_start = game

        # loop as long as we can still move
        while game.canMove() :
            print game
            try :
                origin = int(raw_input("Move from position [-1|1-24]: "))-1
                die = int(raw_input("With die " + str(game.dice) + ": "))
                game = game.move(origin, die)
            except Exception, e :
                print e

        # no more moves possible at this point, if there's still dice left
        # we must check that there was no alternative where more dice were used
        if game.dice and \
            any(( len(g.dice) < len(game.dice) for g in turn_start.nexts() )) :

            print "Restarting turn, because there is a move that uses more dice"
            game = turn_start
        else :
            # turn is complete, throw and continue the game
            print "asdf"
            game.throw()

    print "Game Over!",
    if game.winner() == -1 :
        print "Black has won!"
    else :
        print "White has won!"

