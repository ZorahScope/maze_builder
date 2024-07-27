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
    # test lines
    line1 = Line(Point(100, 50), Point(700, 300))
    line2 = Line(Point(200, 50), Point(500, 500))
    line3 = Line(Point(350, 150), Point(200, 400))
    win.draw_line(line1, "red")
    win.draw_line(line2, "blue")
    win.draw_line(line3, "green")
    win.wait_for_close()


main()
