from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, x1: int, x2: int, y1: int, y2: int, win):
        if x1 == x2 or y1 == y2:
            raise ValueError("Cell must be a square/rectangle")

        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self) -> None:
        corners = self.map_corners()
        canvas = self._win.canvas

        if self.has_left_wall:
            Line(corners["top-left"], corners["bottom-left"]).draw(canvas, "black")
        if self.has_top_wall:
            Line(corners["top-left"], corners["top-right"]).draw(canvas, "black")
        if self.has_right_wall:
            Line(corners["top-right"], corners["bottom-right"]).draw(canvas, "black")
        if self.has_bottom_wall:
            Line(corners["bottom-left"], corners["bottom-right"]).draw(canvas, "black")

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
    win = Window(800, 600)
    # test lines and cells
    line1 = Line(Point(100, 50), Point(700, 300))
    line2 = Line(Point(200, 50), Point(500, 500))
    line3 = Line(Point(350, 150), Point(200, 400))
    win.draw_line(line1, "red")
    win.draw_line(line2, "blue")
    win.draw_line(line3, "green")

    cell1 = Cell(100, 200, 100, 200, win)
    cell1.has_bottom_wall = False
    cell1.draw()

    cell2 = Cell(250, 350, 250, 350, win)
    cell2.has_right_wall = False
    cell2.draw()

    win.wait_for_close()


main()
