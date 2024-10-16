from graphics import Window
from cell import Cell
from time import sleep
import random


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
        seed: int = None,
        sleep_interval: int = 0.05,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed:
            random.seed(seed)
        self._sleep = sleep_interval

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        if not self._win:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if not self._win:
            return

        self._win.redraw()
        sleep(self._sleep)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]

        entrance_cell.has_top_wall = False

        exit_cell.has_bottom_wall = False

        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i: int, j: int):
        if i < 0 or j < 0 or i >= self._num_cols or j >= self._num_rows:
            return
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            choices = []
            up = None
            right = None
            down = None
            left = None

            if j - 1 >= 0:
                up = self._cells[i][j - 1]
            if i + 1 < self._num_cols:
                right = self._cells[i + 1][j]
            if j + 1 < self._num_rows:
                down = self._cells[i][j + 1]
            if i - 1 >= 0:
                left = self._cells[i - 1][j]

            if up and not up.visited:
                choices.append("up")
            if right and not right.visited:
                choices.append("right")
            if down and not down.visited:
                choices.append("down")
            if left and not left.visited:
                choices.append("left")

            if not choices:
                self._draw_cell(i, j)
                return

            pick = random.choice(choices)
            direction_map = {
                "up": (up, ("top_wall", "bottom_wall"), (0, -1)),
                "right": (right, ("right_wall", "left_wall"), (1, 0)),
                "down": (down, ("bottom_wall", "top_wall"), (0, 1)),
                "left": (left, ("left_wall", "right_wall"), (-1, 0)),
            }

            next_cell, walls, (di, dj) = direction_map[pick]
            setattr(cell, f"has_{walls[0]}", False)
            setattr(next_cell, f"has_{walls[1]}", False)

            self._break_walls_r(i + di, j + dj)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int):
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        direction_map = {
            "up": (("top_wall", "bottom_wall"), (0, -1)),
            "right": (("right_wall", "left_wall"), (1, 0)),
            "down": (("bottom_wall", "top_wall"), (0, 1)),
            "left": (("left_wall", "right_wall"), (-1, 0)),
        }

        for key in direction_map.keys():
            walls, (di, dj) = direction_map[key]
            if 0 <= i + di < self._num_cols and 0 <= j + dj < self._num_rows:
                next_cell = self._cells[i + di][j + dj]
                if (
                    not next_cell.visited
                    and getattr(cell, f"has_{walls[0]}") == False
                    and getattr(next_cell, f"has_{walls[1]}") == False
                ):
                    cell.draw_move(next_cell)
                    if self._solve_r(i + di, j + dj):
                        return True
                    else:
                        cell.draw_move(next_cell, True)

        return False
