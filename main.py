from graphics import Window, Line, Point

line = Line(Point(0, 0), Point(100, 100))

win = Window(800, 600)
win.draw_line(line, "red")
win.wait_for_close()
