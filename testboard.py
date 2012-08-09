import board
from traversal_runner import *


class TestBoard(board.Board):
    def __init__(self, matrix, previous_matrix=None):
        board.Board.__init__(self, len(matrix[0]))
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                self.a[i][j].color = matrix[i - 1][j - 1]
        if previous_matrix != None:
            self.previous_board = board.Board._copy_board(self.a)
            for i in range(1, self.size + 1):
                for j in range(1, self.size + 1):
                    self.previous_board[i][j].color = \
                        previous_matrix[i - 1][j - 1]
                
    def assert_same_colors(self, matrix):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.a[i][j].color != matrix[i - 1][j - 1]:
                    return False
        return self._ensure_clean_traversal()
        
    def assert_same_chains(self, matrix):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.a[i][j].chain_id != matrix[i - 1][j - 1]:
                    return False
        return True
    
    def _ensure_clean_traversal(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.a[i][j].traversed == True:
                    return False
        return True
