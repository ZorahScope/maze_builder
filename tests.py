import unittest
from main import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells2(self):
        num_cols = 15
        num_rows = 15
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_zero_cells(self):
        num_cols = 0
        num_rows = 0
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        
        self.assertEqual(
            len(m1._cells),
            num_cols,
            num_rows
        )

    def test_break_entrance_and_exit(self):
        num_cols = 5
        num_rows = 5
        test_maze = Maze(0, 0, num_rows, num_cols, 10, 10) 
        
        self.assertEqual(
            False,
            test_maze._cells[0][0].has_left_wall,
            test_maze._cells[-1][-1].has_right_wall,
        )

        
if __name__ == '__main__':
    unittest.main()
