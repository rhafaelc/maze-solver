from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color="black"):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()
        print("closed")

    def close(self):
        self.__is_running = False

    def draw_line(self, line: Line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
