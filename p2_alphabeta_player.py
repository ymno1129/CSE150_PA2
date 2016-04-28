# -*- coding: utf-8 -*-
__author__ = 'Dan'
__email__ = 'daz040@eng.ucsd.edu'

from assignment2 import Player, State, Action
from collections import defaultdict

tTable = defaultdict(lambda: None) #transposition table

class AlphaBetaPlayer(Player):
    def __init__(self):
        self.count = 0
        self.bestMove = None
        self.cache ={}

    def alphabeta(self, state, a, b, isMax):
        #if is terminal state, return the utility value
        if state.is_terminal():
            utility = (state.board[self.myGoalIdx] -
                    state.board[self.myOpponentIdx])
            return utility

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
                self.count = self.count + 1
                nextState = state.result(x)
                tmpBest = self.alphabeta(nextState, a, b, False)
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
                self.count = self.count + 1
                nextState = state.result(x)
                tmpBest = self.alphabeta(nextState, a, b, True)
                if tmpBest < v:
                    v = tmpBest
                tTable[(tTable[state], state.player_row)] = min((tTable[state], state.player_row), v) #store best value seen so far
                b = min(b, v)
                if b <= a:
                    break
            return v

    def move(self, state):
# Some experiments of printing, for the purpose of knowing the attributes.
#       next_actions = state.actions()
#       next_states = list()
#       for x in next_actions:
#       next_states.append(state.result(x))
#       print state.board
#       print state.player_row
#       print state.player_goal_idx
#       print state.board[state.opponent_goal_idx]

        next_actions = state.actions()
        if len(next_actions) == 0:
            return
        self.myGoalIdx = state.player_goal_idx
        self.myOpponentIdx =state.opponent_goal_idx
        result = self.alphabeta(state, -100, +100, True)
        return self.bestMove 
        """
        Calculates the best move from the given board using the alphabeta
        algorithm.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """
        raise NotImplementedError("Need to implement this method")
