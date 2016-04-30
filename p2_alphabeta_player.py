# -*- coding: utf-8 -*-
__author__ = 'Dan'
__email__ = 'daz040@eng.ucsd.edu'

from assignment2 import Player, State, Action
from collections import defaultdict

class AlphaBetaPlayer(Player):
    def __init__(self):
        self.bestMove = None
        self.cache ={}
        self.table = {}

    def alphabeta(self, state, a, b, isMax):
        key = state.ser()

        if state.is_terminal():
            utility = (state.board[self.myGoalIdx] -
                    state.board[self.myOpponentIdx])
            return utility

        next_actions = state.actions()
        if len(next_actions) == 0:
            isMax = not isMax
            state.player_row = state.opponent_row

        if isMax:
            bestMove = None
            next_actions = state.actions()
            for x in next_actions:
                nextState = state.result(x)
                tmpBest = self.alphabeta(nextState, a, b, False)
                if tmpBest > a:
                    a = tmpBest
                    bestMove = x
                if a >= b:
                    break
            self.bestMove = bestMove
            self.cache[(key, isMax)] = a
            return a

        else:
            next_actions = state.actions()
            for x in next_actions:
                nextState = state.result(x)
                tmpBest = self.alphabeta(nextState, a, b, True)
                if tmpBest < b:
                    b = tmpBest
                if b <= a:
                    break
            self.cache[(key, isMax)] = b
            return b

    def move(self, state):
        next_actions = state.actions()
        if len(next_actions) == 0:
            return

        if state.ser() in self.table:
            return self.table[state.ser()]

        self.myGoalIdx = state.player_goal_idx
        self.myOpponentIdx =state.opponent_goal_idx

        result = self.alphabeta(state, -1000, +1000, True)

        self.table[state.ser()] = self.bestMove

        return self.bestMove 
        """
        Calculates the best move from the given board using the alphabeta
        algorithm.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """
        raise NotImplementedError("Need to implement this method")
