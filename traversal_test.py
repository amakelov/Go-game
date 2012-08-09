import unittest
from traversal_runner import *
import testboard

inputs = [[[0, 1, 0, 0, 1, 1, 2, 0, 0], \
           [1, 0, 0, 1, 1, 2, 0, 0, 0], \
           [2, 1, 1, 1, 2, 2, 2, 0, 0], \
           [2, 2, 0, 2, 2, 2, 0, 2, 0], \
           [0, 0, 2, 0, 1, 1, 2, 0, 0], \
           [2, 2, 2, 2, 1, 0, 1, 2, 2], \
           [2, 2, 1, 1, 0, 1, 0, 1, 2], \
           [2, 1, 1, 0, 0, 0, 0, 1, 1], \
           [1, 1, 0, 0, 0, 0, 0, 0, 0]], \
           
          [[1, 1, 1, 2, 0, 2, 1, 0, 1], \
           [1, 1, 1, 2, 0, 2, 1, 1, 0], \
           [1, 1, 2, 2, 0, 2, 2, 1, 1], \
           [2, 2, 2, 0, 0, 0, 2, 1, 0], \
           [0, 0, 0, 0, 0, 0, 2, 1, 1], \
           [2, 2, 0, 0, 0, 0, 2, 2, 2], \
           [1, 2, 2, 2, 2, 0, 2, 1, 1], \
           [0, 1, 1, 1, 2, 0, 2, 1, 0], \
           [1, 1, 0, 1, 2, 0, 2, 1, 1]],
           
          [[0, 2, 0, 0, 0, 0, 0, 0, 0], \
           [2, 1, 2, 2, 0, 0, 0, 0, 0], \
           [2, 1, 1, 1, 2, 0, 0, 0, 0], \
           [2, 1, 2, 1, 2, 0, 0, 0, 0], \
           [2, 1, 1, 2, 0, 0, 0, 0, 0], \
           [0, 2, 2, 0, 2, 2, 2, 0, 0], \
           [0, 0, 0, 2, 1, 1, 1, 2, 0], \
           [0, 0, 0, 2, 1, 0, 1, 2, 0], \
           [0, 0, 0, 2, 1, 0, 1, 2, 0]]]

class TraversalTest(unittest.TestCase):

    def test_check_chain_liberties(self):       
                   
        chain_heads = [(8, 2), (1, 1), (2, 2)]
        results = [True, False, False]
        for i in range(0, len(results)):
            tb = testboard.TestBoard(inputs[i])
            self.assertEqual(results[i], TraversalRunner.\
                check_chain_liberties(tb.a, chain_heads[i][0], \
                    chain_heads[i][1]))
                    
    def test_form_chains(self):
        outputs = [[[0, 1, 2, 2, 3, 3, 4, 5, 5], \
                    [6, 2, 2, 3, 3, 7, 5, 5, 5], \
                    [8, 3, 3, 3, 7, 7, 7, 5, 5], \
                    [8, 8, 9, 7, 7, 7, 10, 11, 5], \
                    [12, 12, 13, 14, 15, 15, 16, 5, 5], \
                    [13, 13, 13, 13, 15, 17, 18, 19, 19], \
                    [13, 13, 20, 20, 21, 22, 21, 23, 19], \
                    [13, 20, 20, 21, 21, 21, 21, 23, 23], \
                    [20, 20, 21, 21, 21, 21, 21, 21, 21]]]
        
        for i in range(0, len(outputs)):
            tb = testboard.TestBoard(inputs[i])
            TraversalRunner.form_chains(tb.a)
            self.assertTrue(tb.assert_same_chains(outputs[i]))                  
                
        
    
if __name__ == "__main__":
    unittest.main()
