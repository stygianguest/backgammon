from random import randint

BOARD_LENGTH = 4 * 6
NO_DICE = 2
DICE_SIZE = 6

class Game :
    def __init__(self) :
        self.board = [ 0 for i in range(BOARD_LENGTH) ]

        # negative token is black, positive white
        for (i,n) in enumerate([6,5,6,3]) :
            self.board[i*6] = n
            self.board[-i*6-1] = -n

        # self.tokens[player] are the number of off-game tokens of player {1,-1}
        # since this isn't shared token count is always positive
        self.side = [0,0]

        # players 1 and -1 (used for step direction)
        self.player = -1
        self.throw()

    def throw(self) :
        self.player = -self.player
        self.moves = [ randint(1,DICE_SIZE) for i in range(NO_DICE) ]

        if all((self.moves[0] == i for i in self.moves )) :
            # if the dice are the same, double the moves
            self.moves = self.moves * 2

    def move(self, actions) :
        # the pairs (t,s) in actions are commands that move the token at t s
        # steps where the direction depends on the current player offside
        # tokens have position -1

        if len(filter(lambda t : t == -1, tokens)) < min(len(self.moves), 
                self.side[self.player]) :
            return "Must move as many tokens as possible from the side first"

        if any(( self.board[o]*self.player <= 0
                for (o,d) in actions if o >= 0 )) :
            return "Can only move from a position where current player has a token"

        if any(( self.player * (self.board[d] + self.player) < 0 
                for (o,d) in actions)) :
            return "Can only move on top of at most one token of the other player"

        # execute the actions
        for (o,d) in actions :
            self.board[o] -= self.player
            if self.board[d] * self.player == 1 :
                # stepping on top of someone: remove the token first
                self.board[d] = 0
                self.side[-self.player] += 1
            self.board[d] += self.player
        
        #TODO: check if all moves are utilized

        # prepare for the next move
        self.throw()
        
        return None

    def possible(self) :
        ps = []
        for move in self.moves :
            for o in range(-1, len(self.board)) :
                if o == -1 and self.side[self.player] <= 0
                        or self.board[o]*self.player <= 0 :
                    # Can only move from a position where player has a token
                    continue

                if o == 
                    # Must move as many tokens as possible from the side first
                    continue

                if any(( self.player * (self.board[d] + self.player) < 0 
                        for (o,d) in actions)) :
                    # Can only move on top of at most one another player's token
                    continue

    def __str__(self) :
        s = str(self.side[-1]) + " "
        if self.player == -1 :
            s += str(self.moves)
        s += "\n"
        s += concat(intersperse(map(str, self.board[18:24][::-1]), " "))
        s += "\t"
        s += concat(intersperse(map(str, self.board[12:18][::-1]), " "))
        s += "\n"
        s += concat(intersperse(map(str, self.board[0:6]), " "))
        s += "\t"
        s += concat(intersperse(map(str, self.board[6:12]), " "))
        s += "\n"
        s += str(self.side[1]) + " "
        if self.player == 1 :
            s += str(self.moves)

        return s


def concat(lsts) :
    if type(lsts[0]) is str :
        return reduce(str.__add__, lsts)

    return [ i for lst in lsts for i in lst ]

def intersperse(lst, sep) :
    if not list :
        return lst
    return concat([ (i,sep) for i in lst[:-1] ]) + [lst[-1]]

g = Game()
print g
print g.move([0,0])
print g

