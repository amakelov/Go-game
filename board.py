"""
This module contains the implementation of 'the board'.

Class Board provides public methods:
__init__(self, size)
place_at(self, i, j, color)
get_result(self)

The board is represented by two-dimensional array of objects from
class Square. This implementation could be easily changed as
class Game uses only the public interface.

Class Board defines the logic for the algorithms while their concrete
implementation is in the helper class - TraversalRunner

"""

from traversal_runner import *


ENGAGED = -1
SUICIDE = -2
REPETITION = -3

            
class Square:
    def __init__(self, color):
        self.color = color
        self.traversed = False
        self.chain_id = -1
        
    def _get_color(self):
        if self.color == 0:
            return 'o'
        elif self.color == 1:
            return 'B'
        elif self.color == 2:
            return 'W'
        elif self.color == -1:
            return '#'
        else:
            raise ValueError('Invalid square color')
            
            
class Chain:
    def __init__(self, id, head, count, color):
        self.id = id
        self.head = head
        self.count = count
        self.color = color
        self.neighbours = set()
        

class Board:
    def __init__(self, size):
        self.size = size
        self.previous_board = None
        self.a = [[Square(0) for i in range(0, self.size + 2)] \
            for j in range(0, self.size + 2)]
        for i in range(0, self.size + 2):
            self.a[i][0].color = -1
        for i in range(0, self.size + 2):
            self.a[i][self.size + 1].color = -1
        for i in range(0, self.size + 2):
            self.a[0][i].color = -1
        for i in range(0, self.size + 2):
            self.a[self.size + 1][i].color = -1 
    
    @staticmethod        
    def _copy_board(b):
        return list(list(Square(sq.color) for sq in row) for row in b)
        
    @staticmethod
    def _are_equal_boards(b1, b2):
        if b1 == None or b2 == None:
            return False
        for i in range(0, len(b1)):
            for j in range(0, len(b1)):
                if b1[i][j].color != b2[i][j].color:
                    return False
        return True
    
    @staticmethod        
    def adjacent(i, j):
        return ((i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j))        
  
    """def print_board(self):
        print('')
        ''.join(str(i).rjust(3) for i in range(1, self.size + 1))
       """        
        
    def print_board(self):
        print('')      
        print('  ', *[j for j in range(1, min(self.size + 1, 10))], \
            sep = '  ', end = '')
        print(' ', *[j for j in range(10, self.size + 1)], sep = ' ') 
           
        for i in range(1, self.size):
            print(i, '  ' if i < 10 else ' ', end = '')
            print(*[self.a[i][j]._get_color() \
                    for j in range(1, self.size + 1)], sep = '--')              
            print('  ', *['|' for j in range(1, self.size + 1)], sep = '  ')
        print(self.size, ' ', end = '')
        print(*[self.a[self.size][j]._get_color() \
                    for j in range(1, self.size + 1)], sep = '--')
        print('')
        
    def _print_board(self, b):
        print('')      
        print('  ', *[j for j in range(0, min(self.size + 2, 10))], \
            sep = '  ', end = '')
        print(' ', *[j for j in range(10, self.size + 2)], sep = ' ') 
           
        for i in range(0, self.size + 1):
            print(i, '  ' if i < 10 else ' ', end = '')
            print(*[b[i][j]._get_color() \
                    for j in range(0, self.size + 2)], sep = '--')              
            print('  ', *['|' for j in range(0, self.size + 2)], sep = '  ')
        print(self.size+1, ' ', end = '')
        print(*[b[self.size+1][j]._get_color() \
                    for j in range(0, self.size + 2)], sep = '--')
        print('')
    
      
    def print_board_chains(self, b):
        """
        Print the number of the chain for each square.
        
        Used to show chains when determining which groups are dead.
        
        """
        print('')      
        print('  ', *[j for j in range(1, min(self.size + 1, 10))], \
            sep = '  ', end = '')
        print(' ', *[j for j in range(10, self.size + 1)], sep = ' ') 
           
        for i in range(1, self.size):
            print(i, '  ' if i < 10 else ' ', end = '')
            print(*[b[i][j].chain_id \
                    for j in range(1, self.size + 1)], sep = '--')              
            print('  ', *['|' for j in range(1, self.size + 1)], sep = '  ')
        print(self.size, ' ', end = '')
        print(*[b[self.size][j].chain_id \
                    for j in range(1, self.size + 1)], sep = '--')
        print('')
        
                
    def get_result(self):
        """
        Return result if the current positions on the board are final.
        
        Detect and remove dead groups and counts territories for each player.
        Used criteria: a group is considered dead if it has only one 
        neighbour chain with color 0 (free squares) and this neighbour consists
        of 1 or 2 or 4 squares forming the shape 'square'.
        (This means the group is unable to form two eyes).
        
        """
        b = Board._copy_board(self.a)
        
        # perform partition of the squares in chains
        chains = TraversalRunner.form_chains(b)
        
        # find the neighbours for each chain     
        for chain in chains:
            TraversalRunner.mark_neighbours(\
                
                b, chain.head[0], chain.head[1], chains)
            
        # debug
        # print('before removing dead')
        # self.print_board_chains(b)        
        
        TraversalRunner.clean_traversal(b)               
        
        prisoners = [0, 0]
        territories = [0, 0]
        
        # remove dead chains       
        for chain in chains:
            if chain.count == 0:
                continue
            (i, j) = chain.head
                        
            if chain.color == 0 and (chain.count in [1, 2] or
                chain.count == 4 and \
                b[i][j + 1].color == b[i + 1][j].color == \
                b[i + 1][j + 1].color == chain.color):
                
                print('bad shape', chain.id)
                copied_neighbours = set(chain.neighbours)
                for n_id in copied_neighbours:
                    n_chain = chains[n_id]
                    free_neighbours = [id for id in n_chain.neighbours \
                        if chains[id].color == 0]
                    if len(free_neighbours) == 1:
                        print('dies chain:', n_id)
                        if n_chain.color == 1:
                            prisoners[1] += n_chain.count
                        else:
                            prisoners[0] += n_chain.count
                            
                        chain.count += n_chain.count
                        n_chain.count = 0
                        TraversalRunner.traverse_chain(b, n_chain.head[0], \
                            n_chain.head[1], chain.id, chain.color)
                        TraversalRunner.clean_traversal(b)
                            
                        n_chain.neighbours.remove(chain.id)
                        #print('dead chain id, neighbours:', \
                        #    n_chain.id, *n_chain.neighbours)
                        
                        for n_id1 in n_chain.neighbours:
                            chains[n_id1].neighbours.remove(n_id)
                            chains[n_id1].neighbours.add(chain.id)
                                                        
                        chain.neighbours.remove(n_id)
                        chain.neighbours = \
                            chain.neighbours.union(n_chain.neighbours)
                        #print('expanded chain id, nb', chain.id, \
                        #    *chain.neighbours)
        
        # self.print_board_chains(b)
                
        for chain in chains:
            if chain.color == 0:
                n_colors = set([chains[id].color for id in chain.neighbours])
                if len(n_colors) == 1:
                    if 1 in n_colors:
                        territories[0] += chain.count
                    else:
                        territories[1] += chain.count
                        
        return [prisoners, territories]                
                    
                    
    def place_at(self, i, j, color):
        """
        Try to place a piece of this color at square (i, j).
        
        If this move is illegal, return -1.
        Else return the number of captured prisoners.
        
        This method ensures that 'ko' rule is not broken.
        (Players are not allowed to make a move that returns the game
        in the previous position)
        
        """
        current_board = Board._copy_board(self.a)
        res = self._place_at(i, j, color)
        if res in [ENGAGED, SUICIDE]:
            return res
        
        #print('prev:')
        #self._print_board(self.previous_board)
        #print('after illegal move')
        #self._print_board(self.a)
        
        if Board._are_equal_boards(self.previous_board, self.a):
            self.a = current_board
            return REPETITION
        
        self.previous_board = current_board 
        
        return res
        
    def _place_at(self, i, j, color):
        """
        Try to place a piece of this color at square (i, j).
        
        If this move is illegal(the position is occupied or
        it is a suicide), return -1.
        Else make the move and return the number of captured prisoners.
        
        """
        if self.a[i][j].color != 0:
            return ENGAGED
                
        self.a[i][j].color = color
        prisoners = TraversalRunner.capture(self.a, i, j, color)
        
        # ban suicide
        if prisoners == 0:
            has_liberties = \
                TraversalRunner.check_chain_liberties(self.a, i, j)
            TraversalRunner.clean_traversal(self.a)
            if has_liberties == False:   
                self.a[i][j].color = 0
                return SUICIDE
        
        return prisoners
    
    
        
        
        





























        
            
        
