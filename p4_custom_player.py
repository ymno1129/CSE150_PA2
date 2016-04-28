# -*- coding: utf-8 -*-

__author__ = 'Dan'
__email__ = 'daz040@eng.ucsd.edu'

from assignment2 import Player
from collections import defaultdict

tTable = defaultdict(lambda: None) #transposition table

class CustomPlayer(Player):
    '''
    Evaluation function
    '''
    def evaluate(self, state, my_row):
        value = 0
        soms = 0 #stones on my side
        soos = 0 #stones on opponent side
        simg = 0 #stones in my goal
        siog = 0 #stones in opponent goal
        if my_row == 0:
            simg = state.board[state.M]
            siog = state.board[(2 * state.M + 1)]
            for x in range (0, state.M):
                 soms = soms + state.board[x]
                 soos = soos + state.board[(2 * state.M - x)]
        else:
            simg = state.board[(2 * state.M + 1)]
            siog = state.board[state.M]
            for x in range (state.M + 1, 2 * state.M + 1):
                 soms = soms + state.board[x]
                 soos = soos + state.board[(2 * state.M - x)]
        value = simg - siog
        value = value + soms - soos
        value = float(value) / (2 * state.M * state.N)
        return value

    '''
    Alphabeta
    '''
    def alphabeta(self, state, a, b, isMax, depth):
        #if is terminal state, return the utility value
        if state.is_terminal():
            utility = (state.board[self.myGoalIdx] -
                    state.board[self.myOpponentIdx])
            return utility

        if depth > self.maxDepth:
            value = self.evaluate(state, state.player_row)
            return value
        #get possible next actions, if there is no action
        #then it means the player playing on this row cannot
        #move at this turn, so switch row and turn.
        next_actions = state.actions()
        if len(next_actions) == 0:
            isMax = not isMax
            state.player_row = state.opponent_row

        if tTable[(state, state.player_row)]: # if previously seen state, return the utility of that state
            return tTable[(tTable[state], state.player_row)]

        #If is max(player himself), pick max value and run min
        if isMax:
            bestMove = None
            v = -100
            next_actions = state.actions()
            for x in next_actions:
                nextState = state.result(x)
                tmpBest = self.alphabeta(nextState, a, b, False, depth + 1)
                if tmpBest > v:
                    v = tmpBest
                    bestMove = x
                tTable[(tTable[state], state.player_row)] = max((tTable[state], state.player_row), v) #store best value seen so far
                a = max(a, v)
                if b <= a:
                    break
            self.bestMove = bestMove
            return v

        #If is min(opponent), pick min value and run max
        else:
            v = +100
            next_actions = state.actions()
            for x in next_actions:
                nextState = state.result(x)
                tmpBest = self.alphabeta(nextState, a, b, True, depth + 1)
                if tmpBest < v:
                    v = tmpBest
                tTable[(tTable[state], state.player_row)] = min((tTable[state], state.player_row), v) #store best value seen so far
                b = min(b, v)
                if b <= a:
                    break
            return v


    def __init__(self):
        self.tmpBestMove = None
        self.tmpBestResult = None
        self.bestMove = None
        self.bestResult = None
        self.maxDepth = 0
        self.table = {}
        pass

    def move(self, state):
        actions = state.actions()
        if len(actions) == 0:
            return 

        self.myGoalIdx = state.player_goal_idx
        self.myOpponentIdx = state.opponent_goal_idx

        for x in range (0, 10):
            self.maxDepth = x
            result = self.alphabeta(state, -1000, 1000, True, 0)
            if self.tmpBestResult == None:
                self.tmpBestResult = result
                self.bestMove = self.tmpBestMove
            else:
                if result > self.tmpBestResult:
                    self.tmpBestResult == result
                    self.bestMove = self.tmpBestMove

        self.table[state.ser()] = self.bestMove

        return self.bestMove
 
        raise NotImplementedError("Need to implement this method")

