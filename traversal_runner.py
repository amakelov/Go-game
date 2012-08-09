#from board import *
#from board import Chain
import board
       
def adjacent(i, j):
    return ((i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j))  

class TraversalRunner:
    """
    Provides implementations of different traversals - used are dfs or bfs.
    
    It could be easily extended with other implementations or the existing
    could be optimized.
    
    """     
    @staticmethod
    def clean_traversal(b):
        for row in b:
            for sq in row:
                sq.traversed = False
                
    @staticmethod    
    def check_chain_liberties(b, i, j):
        b[i][j].traversed = True
        for n in adjacent(i, j):
            if b[n[0]][n[1]].color == 0:
                return True
            if b[n[0]][n[1]].color == b[i][j].color and \
                b[n[0]][n[1]].traversed == False:
                    if(TraversalRunner.check_chain_liberties(b, n[0], n[1])):
                        return True
        return False
        
    @staticmethod                
    def traverse_chain(b, i, j, id, color=None):         
        b[i][j].traversed = True
        b[i][j].chain_id = id
        count = 1
        for n in adjacent(i, j):
            if b[n[0]][n[1]].color == b[i][j].color and \
                    b[n[0]][n[1]].traversed == False:              
               
                count += TraversalRunner.traverse_chain(b, n[0], n[1], id)
                
        if color != None:
            b[i][j].color = color
        return count
        
    @staticmethod
    def form_chains(b):
        chains = []
        id = 0
        for i in range(1, len(b) - 1):
            for j in range(1, len(b) - 1):
                if b[i][j].traversed == False:
                    count = TraversalRunner.traverse_chain(b, i, j, id)
                    chains.append(board.Chain(id, (i, j), count, \
                        b[i][j].color))
                    id += 1
                    
        TraversalRunner.clean_traversal(b)
        return chains
    
    @staticmethod  
    def mark_neighbours(b, i, j, chains):
        b[i][j].traversed = True
        for n in adjacent(i, j):
            if b[n[0]][n[1]].color not in (-1, b[i][j].color):
                chains[b[i][j].chain_id].neighbours.add(b[n[0]][n[1]].chain_id)
                
            elif b[n[0]][n[1]].color == b[i][j].color and \
                    b[n[0]][n[1]].traversed == False:         
                TraversalRunner.mark_neighbours(b, n[0], n[1], chains) 
                
    @staticmethod
    def capture(b, i, j, new_color):
        other_color = 1 if new_color == 2 else 2
        q = []
        prisoners = 0
        for n in adjacent(i, j):
            prisoners += TraversalRunner._capture_direction( \
                    b, n[0], n[1], other_color, q)
        for sq in q:
            b[sq[0]][sq[1]].traversed = False
        return prisoners
    
    @staticmethod    
    def _capture_direction(b, i, j, color, q):
        
        if b[i][j].color != color or b[i][j].traversed == True:
            return 0
        # start index    
        start = l = len(q)
        lev = l + 1
        q.append((i, j))
        b[i][j].traversed = True
        saved = False
                
        while l < len(q):
            for k in range(l, lev):
                sq = q[k]
                for n in adjacent(sq[0], sq[1]):
                    if b[n[0]][n[1]].color == 0 and \
                            b[n[0]][n[1]].traversed == False:
                        return 0
                    elif b[n[0]][n[1]].color == color and \
                            b[n[0]][n[1]].traversed == False:
                        q.append((n[0], n[1]))
                        b[n[0]][n[1]].traversed = True
                
            l = lev
            lev = len(q)
        
        for k in range(start, len(q)):
            sq = q[k]
            b[sq[0]][sq[1]].color = 0
        return len(q) - start
