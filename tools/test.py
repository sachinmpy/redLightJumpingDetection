import turtle
import random
import math

from detectionengine import Point, are_intersecting, Line, is_point_on_line

screen = turtle.getscreen()
# screen.delay(1)
screen.tracer(-1)

pen = turtle.Turtle()
pen.hideturtle()
pen.pensize(5)
# pen.speed(0)


def draw_line(line: Line, color: str = "black") -> None:
    pen.penup()
    pen.color(color)
    pen.goto(line.point_1.x, line.point_1.y)
    pen.pendown()
    pen.goto(line.point_2.x, line.point_2.y)


def draw_point(point: Point, color: str = "black") -> None:
    pen.penup()
    pen.color(color)
    pen.goto(point.x, point.y)
    pen.pendown()
    pen.dot(5)


if __name__ == "__main__":
    print("TESTING")
    offset = 50

    # left = Line(Point(50, 50), Point(50, 150))
    # top = Line(Point(50, 150), Point(150, 150))
    # right = Line(Point(150, 150), Point(150, 50))
    # bottom = Line(Point(150, 50), Point(50, 50))
    #
    # draw_line(left)
    # draw_line(top)
    # draw_line(bottom)
    # draw_line(right)

    line_1 = Line(Point(50, 50), Point(300, 300))
    line_2 = Line(Point(50, 150), Point(0, 200))
    draw_line(line_1, color="pink")
    # draw_line(line_2, color="pink")


    # line_2 = Line(Point(0, 0), Point(100, 0))
    # draw_line(line_2)
    c = 1
    for x in range(0, 500, 7):
        for y in range(0 + x, 100 + x, 7):
            point = Point(x, y - 50)

        # c += math.sin(c)
        # point = Point(y, y + 10)
            intersection_1 = is_point_on_line(line_1, point, tolerance=1)
        # # intersection_2 = are_intersecting(line, line_2)
        #
            if intersection_1:
                draw_point(point, color='black')

            else:
                draw_point(point, color="yellow")

    turtle.mainloop()
