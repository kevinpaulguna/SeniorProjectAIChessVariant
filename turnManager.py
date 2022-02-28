class TurnManager:
    def __init__(self, players=2, actions=3):
        self.players = players
        self.current_player = 1   # who's turn it is currently. starts with 1 because of bool to int translation
        self.max_actions = [actions for _ in range(self.players)]    # number of actions a given team starts with
        self.current_actions = self.max_actions[self.current_player]      # the active players actions left this turn

    def get_current_player(self):
        return self.current_player

    def get_max_actions(self, player):
        return self.max_actions[player]

    def get_current_actions(self, player):
        return self.current_actions

    # if either player runs out of actions on their turns
    # or ends their turn early this moves to next player and resets counters
    def end_turn(self):
        self.current_player += 1
        if self.current_player >= self.players:
            self.current_player = 0
        self.current_actions = self.get_max_actions(self.current_player)

    # this should be called when the current player
    # uses an action on his turn
    def use_action(self):
        self.current_actions -= 1
        if self.current_actions <= 0:
            self.end_turn()

    # removes an action from a player
    # would usually happen on other players
    # turn so you need to specify the player index
    # returns True if game should continue after
    # False otherwise
    def lose_action(self, player_indx):
        self.max_actions[player_indx] = max(self.get_max_actions(player_indx) - 1, 0)




