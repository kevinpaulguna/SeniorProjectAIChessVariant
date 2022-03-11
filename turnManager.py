from ChessGameHelpers import Piece
from ThreeCorp import Corp
class MedievalTurnManager:
    def __init__(self, players=2):
        self.players = players
        # 0 black, 1 white
        self.current_player = 1   # who's turn it is currently. starts with 1 because of bool to int translation
        self.max_actions = [1 for _ in range(self.players)]    # number of actions a given team starts with
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

class CorpCommandTurnManager():
    def __init__(self, players=2):
        self.players = players
        # 0 black, 1 white
        self.current_player = 1   # who's turn it is currently. starts with 1 because of bool to int translation
        self.__delegation_move_used = False

        # initialize corp storage
        self.__corps = {
            'white': [Corp],
            'black': [Corp]
        }

    def get_current_player(self):
        return self.current_player

    # if either player runs out of actions on their turns
    # or ends their turn early this moves to next player and resets counters
    def end_turn(self):
        self.current_player += 1
        if self.current_player >= self.players:
            self.current_player = 0
        self.__reset_turn()

    # this should be called when the current player
    # uses an action on his turn
    def use_action(self, *, piece_used: Piece, small_move:bool):
        if small_move == True:
            print('using commander single space move')
            piece_used.corp.movedOne()
        else:
            print('using command authority')
            piece_used.set_moved()

        self.__update_corps()

        if self.get_number_of_available_moves() <= 0:
            self.end_turn()

    def set_corps(self, *, w1:Corp, w2:Corp, w3:Corp, b1:Corp, b2:Corp, b3:Corp):
        self.__corps['white'] = [w1,w2,w3]
        self.__corps['black'] = [b1,b2,b3]

    def delegation_move_has_been_used(self):
        return self.__delegation_move_used

    def use_delegation_move(self):
        self.__delegation_move_used = True

    # def get_available_moves(self):
    #     corp_color = 'white' if self.current_player else 'black'
    #     return {
    #         1: {
    #             "commandAuth": self.__corps[corp_color][0].hasCommanded(),
    #             "smallMove": self.__corps[corp_color][0].smallMove
    #         },
    #         2: {
    #             "commandAuth": self.__corps[corp_color][1].hasCommanded(),
    #             "smallMove": self.__corps[corp_color][1].smallMove
    #         },
    #         3: {
    #             "commandAuth": self.__corps[corp_color][2].hasCommanded(),
    #             "smallMove": self.__corps[corp_color][2].smallMove
    #         }
    #     }

    def __update_corps(self):
        corp_color = 'white' if self.current_player else 'black'
        for corp in self.__corps[corp_color].copy():
            if not corp.commander:
                self.__corps[corp_color].remove(corp)

    def get_number_of_available_moves(self):
        corp_color = 'white' if self.current_player else 'black'
        count = 0
        for corp in self.__corps[corp_color]:
            if not corp.hasCommanded():
                count += 1
            if not corp.smallMove:
                count += 1
        return count

    def __reset_turn(self):  # Used to reset corp command count for each corp
        self.__delegation_move_used = False
        for wCorp, bCorp in zip(self.__corps['white'], self.__corps['black']):
            wCorp.resetCommand()
            bCorp.resetCommand()
