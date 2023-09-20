class Point:
    def __init__(self, x: float | int, y: int | float) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x, self.y}"

    def get_vectors(self) -> tuple:
        return self.x, self.y


class Line:
    def __init__(self, point_1: Point, point_2: Point):
        self.point_1 = point_1
        self.point_2 = point_2

    def __str__(self):
        return f"{self.point_1}, {self.point_2}"


class Box:
    @staticmethod
    def box_mid_point(points: list[int]) -> Point:
        return Point(
            (points[0] + points[2]) // 2,
            (points[1] + points[3]) // 2,
        )


class Arithmetics:
    pass


if __name__ == "__main__":
    print(Line(Point(1, 2), Point(2, 3)))
