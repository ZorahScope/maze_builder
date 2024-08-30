from tkinter import Tk, BOTH, Canvas
import time
import random
from collections import namedtuple
from typing import Union


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        if canvas:
            canvas.create_line(
                self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
            )


class Cell:
    def __init__(
        self, x1: int = None, x2: int = None, y1: int = None, y2: int = None, win=None
    ):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self) -> None:
        corners = self.map_corners()
        canvas = self._win.canvas if self._win else None

        walls = {
            "left": (self.has_left_wall, corners["top-left"], corners["bottom-left"]),
            "top": (self.has_top_wall, corners["top-left"], corners["top-right"]),
            "right": (
                self.has_right_wall,
                corners["top-right"],
                corners["bottom-right"],
            ),
            "bottom": (
                self.has_bottom_wall,
                corners["bottom-left"],
                corners["bottom-right"],
            ),
        }

        def draw_wall(has_wall, start_corner, end_corner, canvas):
            color = "black" if has_wall else "#d9d9d9"
            Line(start_corner, end_corner).draw(canvas, color)

        for has_wall, start_corner, end_corner in walls.values():
            draw_wall(has_wall, start_corner, end_corner, canvas)

    def map_corners(self) -> dict[str, Point]:
        min_x = min(self._x1, self._x2)
        max_x = max(self._x1, self._x2)
        min_y = min(self._y1, self._y2)
        max_y = max(self._y1, self._y2)

        top_left = Point(min_x, min_y)
        top_right = Point(max_x, min_y)
        bottom_left = Point(min_x, max_y)
        bottom_right = Point(max_x, max_y)

        corners = {
            "top-left": top_left,
            "top-right": top_right,
            "bottom-left": bottom_left,
            "bottom-right": bottom_right,
        }

        return corners

    def map_center(self) -> Point:
        min_x = min(self._x1, self._x2)
        max_x = max(self._x1, self._x2)
        min_y = min(self._y1, self._y2)
        max_y = max(self._y1, self._y2)

        center = Point((max_x + min_x) / 2, (max_y + min_y) / 2)
        return center

    def draw_move(self, to_cell, undo=False) -> None:
        canvas = self._win.canvas
        color = "red" if undo else "gray"

        if to_cell is None or not isinstance(to_cell, Cell):
            raise ValueError("Invalid cell")
        if to_cell is self:
            raise ValueError("Can't use from cell as destination cell")

        from_cell = self.map_center()
        to_cell = to_cell.map_center()
        Line(from_cell, to_cell).draw(canvas, color)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):

        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()
        if seed is not None:
            random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        self._cells = [
            [Cell() for _ in range(self.num_rows)] for _ in range(self.num_cols)
        ]
        for col_count, column in enumerate(self._cells, start=1):
            for row_count, cell in enumerate(column, start=1):
                i = self.x1 + (col_count - 1) * self.cell_size_x
                j = self.y1 + (row_count - 1) * self.cell_size_y
                self._draw_cell(cell, i, j)

    def _draw_cell(self, cell, i, j) -> None:
        i2 = i + self.cell_size_x
        j2 = j + self.cell_size_y
        cell._x1 = i
        cell._y1 = j
        cell._x2 = i2
        cell._y2 = j2
        cell._win = self.win
        cell.draw()
        self._animate()
        return

    def _animate(self) -> None:
        if self.win:
            self.win.redraw()
            time.sleep(0.05)
        return

    def _break_entrance_and_exit(self) -> None:
        if not self._cells:
            return
        entrance = self._cells[0][0]
        exit = self._cells[-1][-1]
        entrance.has_left_wall = False
        exit.has_right_wall = False
        entrance.draw()
        exit.draw()
        return

    def _break_walls_r(self, i, j) -> None:
        if not self._cells:
            return
        self._cells[i][j].visited = True

        def get_adjacent(i2, j2) -> Union[Cell, bool]:
            try:
                if i2 < 0 or j2 < 0:
                    return False
                return self._cells[i2][j2]
            except IndexError:
                return False

        def four_directions(i2, j2) -> dict[str, Cell]:
            # Define directions and their coordinate adjustments
            Grid = namedtuple("Grid", "col row")
            directions = {
                "top": (0, -1),
                "right": (1, 0),
                "bottom": (0, 1),
                "left": (-1, 0),
            }

            adjacent_cells = {}

            for direction, (di, dj) in directions.items():
                loc = Grid(col=i2 + di, row=j2 + dj)
                adjacent = get_adjacent(loc.col, loc.row)
                if adjacent and not adjacent.visited:
                    adjacent_cells[direction] = loc

            return adjacent_cells

        while True:
            valid_directions = four_directions(i, j)
            if not any(valid_directions.values()):
                break
            direction = random.choice(list(valid_directions))
            adj_cell = valid_directions[direction]

            if direction == "top":
                self._cells[i][j].has_top_wall = False
                self._cells[i][j].draw()
                self._cells[adj_cell.col][adj_cell.row].has_bottom_wall = False
                self._cells[adj_cell.col][adj_cell.row].draw()
            if direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i][j].draw()
                self._cells[adj_cell.col][adj_cell.row].has_left_wall = False
                self._cells[adj_cell.col][adj_cell.row].draw()
            if direction == "bottom":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j].draw()
                self._cells[adj_cell.col][adj_cell.row].has_top_wall = False
                self._cells[adj_cell.col][adj_cell.row].draw()
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[i][j].draw()
                self._cells[adj_cell.col][adj_cell.row].has_right_wall = False
                self._cells[adj_cell.col][adj_cell.row].draw()

            self._animate()
            self._break_walls_r(adj_cell.col, adj_cell.row)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Builder")
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.is_running = True

        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line: Line, fill_color):
        line.draw(self.canvas, fill_color)


def main():

    try:
        win = Window(800, 600)
        maze = Maze(50, 50, 15, 15, 30, 30, win, 0)
    except Exception as e:
        print(f"Error: {e}")

    win.wait_for_close()


main()
