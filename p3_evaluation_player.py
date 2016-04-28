# -*- coding: utf-8 -*-
__author__ = 'Dan'
__email__ = 'daz040@eng.ucsd.edu'

from assignment2 import Player, State, Action


class EvaluationPlayer(Player):
    def move(self, state):
        """Calculates the best move after 1-step look-ahead with a simple
        evaluation function.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """

        # *You do not need to modify this method.*
        best_value = -1.0

        actions = state.actions()
        if not actions:
            actions = [None]

        best_move = actions[0]
        for action in actions:
            result_state = state.result(action)
            value = self.evaluate(result_state, state.player_row)
            if value > best_value:
                best_value = value
                best_move = action

        # Return the move with the highest evaluation value
        return best_move

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
        raise NotImplementedError("Need to implement this method")
