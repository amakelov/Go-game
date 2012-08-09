"""
Test the logic for a whole game.

"""
import unittest
import runner
import game
import filecmp


class GameTestCase(unittest.TestCase):
    def test_game(self):
        """
        Test whole games - check final results for a given list of commands.
        
        """
        games = [game.Game('b', 'w', 5)]
        commands = [('3 2', '3 3', '2 1', '2 2', '4 1', '5 1', '5 2', '1 1', \
            'result', 'adf', '1 2', 'help', 'result', '1 2 3', 'pass', \
            '4 3', 'resign')]
        results = [[[2, 0], [4, 0]]]
        
        with open('outfile.txt', 'w') as f:
            for i in range(0, len(games)):
                test_runner = runner.Runner(in_console=False, game=games[i])
                self.assertEqual(results[i], test_runner.play(\
                in_console=False, commands_list=commands[i], outfile=f))
                    
    def test_user_input_validation(self):
        """
        Test class Runner's method play for user input validation.
        Given a list of commands, output is written to a file and compared to
        the content of 'expected.txt'.
        
        """
        commands = ['1 20', '0 1', '1 2 3', 'adk', 'pass', 'help', 'resign']
        g = game.Game('b', 'w', 19)
        test_runner = runner.Runner(in_console=False, game=g)
        with open('outfile.txt', 'w') as f:
            test_runner.play(in_console=False, commands_list=commands, \
                         outfile=f)
        
        self.assertTrue(filecmp.cmp('expected.txt', 'outfile.txt', \
                        shallow=False))
        
        
if __name__ == "__main__":
    unittest.main()
