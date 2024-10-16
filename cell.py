from graphics import Point, Line, Window


class Cell:
    def __init__(
        self,
        win: Window,
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        if not self._win:
            return

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        top_left = Point(self._x1, self._y1)
        top_right = Point(self._x2, self._y1)
        bot_left = Point(self._x1, self._y2)
        bot_right = Point(self._x2, self._y2)

        left_wall = Line(top_left, bot_left)
        top_wall = Line(top_left, top_right)
        right_wall = Line(top_right, bot_right)
        bottom_wall = Line(bot_left, bot_right)

        if self.has_left_wall:
            self._win.draw_line(left_wall)
        else:
            self._win.draw_line(left_wall, "white")

        if self.has_top_wall:
            self._win.draw_line(top_wall)
        else:
            self._win.draw_line(top_wall, "white")

        if self.has_right_wall:
            self._win.draw_line(right_wall)
        else:
            self._win.draw_line(right_wall, "white")

        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall)
        else:
            self._win.draw_line(bottom_wall, "white")

    def draw_move(self, to_cell: "Cell", undo=False):
        cell_center = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        to_cell_center = Point(
            (to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2
        )

        path_line = Line(cell_center, to_cell_center)
        if not undo:
            self._win.draw_line(path_line, "red")
        else:
            self._win.draw_line(path_line, "gray")
