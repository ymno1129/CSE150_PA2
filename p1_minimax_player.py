# -*- coding: utf-8 -*-
__author__ = 'Dan'
__email__ = 'daz040@eng.ucsd.edu'

from assignment2 import Player, State, Action

class MinimaxPlayer(Player):
    def __init__(self):
        self.bestMove = None
        self.cache ={}

    def minimax(self, state, isMax):
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

        #If is max(player himself), pick max value and run min
        if isMax:
            bestMove = None
            bestValue = -100
            next_actions = state.actions()
            for x in range (0,len(next_actions)):
                tmpAction = next_actions[x]
                nextState = state.result(tmpAction)
                tmpBest = self.minimax(nextState, False)
                if tmpBest > bestValue:
                    bestValue = tmpBest
                    bestMove = tmpAction
            self.bestMove = bestMove
            return bestValue

        #If is min(opponent), pick min value and run max
        else:
           bestValue = +100
           next_actions = state.actions()
           for x in next_actions:
               nextState = state.result(x)
               tmpBest = self.minimax(nextState, True)
               if tmpBest < bestValue:
                    bestValue = tmpBest
           return bestValue

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

        self.myGoalIdx = state.player_goal_idx
        self.myOpponentIdx =state.opponent_goal_idx
        result = self.minimax(state, True)
        return self.bestMove 
        """
        Calculates the best move from the given board using the minimax
        algorithm.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """
        raise NotImplementedError("Need to implement this method")
