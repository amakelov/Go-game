import board
import player


class Game:
    """
    Contains the 'game' logic - capsulates info for players'prisoners,
    whose turn it is and the board.
    
    Provided interface:
    __init__(self, black_name, white_name, board_size)
    save_pass(self)
    place_at(self, i, j)
    get_result(self)
    This class could be used by console application or graphic interface.
    
    Board could be any class implementing the following interface:
    place_at(self, i, j, color)
    get_result(self)
    
    """
    
    def __init__(self, black_name, white_name, board_size):
        self.board = board.Board(board_size)
        self.players = [player.Player(1, black_name), \
            player.Player(2, white_name)]
        self.turn = 0  # black's turn
        self.passes = 0
        self.last_passed = False
        
    def _change_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
        
    def save_pass(self):
        self._change_turn() 
        if not self.last_passed:
            self.passes = 1
            self.last_passed = True
        else:
            self.passes = 2
        
    def place_at(self, i, j):
        prisoners = self.board.place_at(i, j, self.players[self.turn].color)
        # if valid move only
        if prisoners >= 0:
            self.players[self.turn].prisoners += prisoners
            self.last_passed = False
            self._change_turn()        
        
        return prisoners
        
    def get_result(self):
        [prisoners, territories] = self.board.get_result()
        prisoners[0] += self.players[0].prisoners
        prisoners[1] += self.players[1].prisoners
        return [prisoners, territories]
        
    def print_result(self):
        [prisoners, territories] = self.get_result()
        print(self.players[0].name, ': prisoners =', prisoners[0], \
            'territory =', territories[0], 'result =', \
            prisoners[0] + territories[0]) 
        print(self.players[1].name, ': prisoners =', prisoners[1], \
            'territory =', territories[1], 'result =', \
            prisoners[1] + territories[1]) 
        
    def get_player(self, turn):
        return self.players[turn]
