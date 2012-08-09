from game import Game
from board import ENGAGED, SUICIDE, REPETITION
import sys

help_message = "Each player should place a piece writing\n" +\
    "i j; you can also write 'pass' or 'resign'\n" +\
    "Typing 'result' shows the current result."
    
class Runner:
    def __init__(self, in_console=True, game=None):
        if in_console:        
            print("Enter your names:")
            black_name = input("Black player: ")
            white_name = input("White player: ")
            board_size = input("Enter board size: ")
            self.game = Game(black_name, white_name, int(board_size))
            print(help_message)
        else:
            self.game = game
       
        
    def play(self, in_console=True, commands_list=None, 
             outfile=sys.stdout):
        #while command != 'resign' and game.passes != 2):
        command_number = 0
        while True:
            if in_console:
                command = input(\
                    self.game.get_player(self.game.turn).name + ': ')
            else:
                command = commands_list[command_number]
                command_number += 1
                
            if command == 'help':
                print(help_message, file=outfile)
            elif command == 'result':
                self.game.print_result()
            elif command == 'resign':
                print(self.game.players[self.game.turn].name, \
                      'lost the game.', file=outfile)
                break
            elif command == 'pass':
                self.game.save_pass()
                if self.game.passes == 2:
                    break        
            else:
                try:
                    command = list(map(int, command.split()))
                    if len(command) != 2:
                        print('Invalid arguments', file=outfile)
                        continue
                    i, j = command
                    
                    if i < 1 or i > self.game.board.size or \
                        j < 1 or j > self.game.board.size:
                        print('Args out of range', file=outfile)
                        continue
                    result = self.game.place_at(i, j)
                    if result < 0:
                        print('Illegal move:', file=outfile)
                        if result == ENGAGED:
                            print('engaged', file=outfile)
                        elif result == SUICIDE:
                            print('suicide', file=outfile)
                        elif result == REPETITION:
                            print('repetition', file=outfile)
                    else:
                        self.game.board.print_board()
                except ValueError:
                    print('Invalid command', file=outfile)    
            
        self.game.print_result()
        return self.game.get_result()
        

if __name__ == '__main__':
    # console_runner = Runner(False, Game('n', 's', 5))
    console_runner = Runner(True)
    console_runner.play()
