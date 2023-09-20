import logging

import cv2
import math
import glob

import time

from imageai.Detection import ObjectDetection
from tools.videoprocessing import Video
from numpy.typing import NDArray
from databaseHandler import RljdDBHandler
from pathlib import Path
from settings import BASE_DIR
from geometry import Point, Line, Box

import os

logger = logging.getLogger(__name__)


db_settings: dict = {  # TODO: to be removed
    "host": "localhost",
    "port": 27017,
    "database": "red-light-jumping-detection",
}


def mid_point(box: list[int]) -> tuple[int, int]:  # TODO: to be removed
    return (box[0] + box[2]) // 2, (box[1] + box[3]) // 2


class Frame:
    # COLORS
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    PURPLE = (0, 0, 125)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    TOLERANCE = 0.5
    RADIUS = 5

    def __init__(self, frame: NDArray, obj_list: list, line: Line):
        self.frame = frame
        self.obj_list = obj_list
        self.line = line
        self.detected_points = []

    def all_mid_points(self) -> tuple[Point]:
        mid_points = []
        for obj in self.obj_list:
            if obj["name"] in ("car", "truck"):
                mid_point: Point = Box.box_mid_point(obj["box_points"])
                mid_points.append(mid_point)

        return tuple(mid_points)

    def place_mid_points(self):
        for point in self.all_mid_points():
            if is_point_on_line(self.line, point, tolerance=self.TOLERANCE):
                cv2.circle(
                    self.frame,
                    point.get_vectors(),
                    radius=self.RADIUS,
                    color=self.WHITE,
                    thickness=-1,
                )
                cv2.line(
                    self.frame,
                    self.line.point_1.get_vectors(),
                    self.line.point_2.get_vectors(),
                    color=self.RED,
                    thickness=3,
                )
                self.detected_points.append(point)
            else:
                cv2.circle(
                    self.frame,
                    point.get_vectors(),
                    radius=self.RADIUS,
                    color=self.BLUE,
                    thickness=-1,
                )


class DetectionEngine:
    model_path = Path.joinpath(BASE_DIR, "AIModels/yolov3.pt")
    print(model_path)
    FPS = 24

    detector: ObjectDetection = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path.as_posix())
    detector.loadModel()

    def __init__(self, url: Path) -> None:
        self.url = url
        self.video: Video = Video(self.url)

    def get_frames_from_video(
        self, frame_count: int = 100, step: int = 1
    ) -> list[NDArray]:
        return self.video.read_frames(frame_count, step)

    def detect_objects_from_frames(self, line_coords: Line) -> list[Frame]:
        frames = self.get_frames_from_video()
        detected_frames = []

        for frame in frames:
            img, detection = self.detector.detectObjectsFromImage(
                frame,
                minimum_percentage_probability=50,
                output_type="array",
            )

            detected_frames.append(Frame(img, obj_list=detection, line=line_coords))

        return detected_frames

    @staticmethod
    def write_to_db(  # TODO: this will go outside
        frames: list[Frame], file_name: str, file_date: str, file_time: str
    ):
        db: RljdDBHandler = RljdDBHandler(db_settings, collection_name="infringement")
        print("Written")
        print(db.current_collection)

        for frame in frames:
            if is_on_mid_point(
                frame,
                frame.line.point_1.get_vectors(),
                frame.line.point_2.get_vectors(),
            ):
                q = {
                    "file_date": file_date,
                    "file_name": file_name,
                    "file_time": file_time,
                }
                db.insert(q)
                print(q)

    @staticmethod
    def construct_video(frames: list[Frame]):
        FRAMES = Path(
            r"C:\Users\smath\PycharmProjects\redLightJumpingDetection\temp_frame"
        )
        delete_files_in_folder(FRAMES)

        color = (125, 0, 0)
        count = 1
        for frame in frames:
            count += 1
            cv2.line(
                frame.frame,
                frame.line.point_1.get_vectors(),
                frame.line.point_2.get_vectors(),
                color=color,
                thickness=3,
            )
            # print(frame.line)
            place_mid_points(
                frame,
                color=(0, 0, 255),
                radius=5,
                point_1=frame.line.point_1.get_vectors(),
                point_2=frame.line.point_2.get_vectors(),
            )
            # print(type(frame.frame))
            cv2.imwrite(rf"{FRAMES}\{count}.jpeg", frame.frame)
        DetectionEngine._show_video_from_frames(frames, delay=0.1)
        DetectionEngine.convert_frames_to_video(
            frames,
            Path(
                r"C:\Users\smath\PycharmProjects\redLightJumpingDetection\videofiles\Final Videos"
            ),
        )  # TODO: Convert to relative path

        return frames

    @staticmethod
    def _show_video_from_frames(frames: list[Frame], delay: float = 0.1):
        for frame in frames:
            cv2.imshow("AI ", frame.frame)
            time.sleep(delay)
            cv2.waitKey(1)

    @staticmethod
    def convert_frames_to_video(frames: list[Frame], path_out: Path) -> None:
        fourcc = cv2.VideoWriter_fourcc(*"DIVX")
        out = cv2.VideoWriter(
            rf"{path_out}\final_vid_1.avi", fourcc, 12, frameSize=(1280, 720)
        )

        FRAMES = Path(
            r"C:\Users\smath\PycharmProjects\redLightJumpingDetection\temp_frame"
        )

        images = glob.glob(
            r"C:\Users\smath\PycharmProjects\redLightJumpingDetection\temp_frame\*.jpeg"
        )
        images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))

        for image in images:
            try:
                # print(f"{frame} was written")
                frame = cv2.imread(image)
                frame = cv2.resize(frame, dsize=(1280, 720))
                out.write(frame)
            except:
                out.release()

        out.release()


class AIWrapper:
    pass


def distance(point_a: Point, point_b: Point) -> float | int:
    ans = abs((point_b.x - point_a.x)) ** 2 + abs((point_b.y - point_a.y)) ** 2

    return math.sqrt(ans)


def is_point_on_line(line: Line, point: Point, tolerance: float) -> bool:
    AB = distance(line.point_1, line.point_2)
    AC = distance(line.point_1, point)
    BC = distance(line.point_2, point)

    return AB - tolerance <= (AC + BC) <= AB + tolerance


def are_intersecting(line_1: Line, line_2: Line) -> tuple[bool, float, float]:
    denominator = (line_2.point_2.y - line_2.point_1.y) * (
        line_1.point_2.x - line_1.point_1.x
    ) - (line_2.point_2.x - line_2.point_1.x) * (line_1.point_2.y - line_1.point_1.y)

    if denominator == 0:
        return False, 0, 0

    numerator_u = (line_2.point_2.x - line_2.point_1.x) * (
        line_1.point_1.y - line_2.point_1.y
    ) - (line_2.point_2.y - line_2.point_1.y) * (line_1.point_1.x - line_2.point_1.x)
    numerator_t = (line_1.point_2.x - line_1.point_1.x) * (
        line_1.point_1.y - line_2.point_1.y
    ) - (line_1.point_2.y - line_1.point_1.y) * (line_1.point_1.x - line_2.point_1.x)

    u = numerator_u / denominator
    t = numerator_t / denominator

    intersection_x = line_1.point_1.x + (u * (line_1.point_2.x - line_1.point_1.x))
    intersection_y = line_1.point_1.y + (u * (line_1.point_2.y - line_1.point_1.y))

    return (0 <= u <= 1) and (0 <= t <= 1), intersection_x, intersection_y


def is_on_mid_point(frame: Frame, point_1: tuple, point_2: tuple):
    for box in frame.obj_list:
        _mid_point = mid_point(box["box_points"])
        _point = Point(_mid_point[0], _mid_point[1])
        if is_point_on_line(
            Line(Point(point_1[0], point_1[1]), Point(point_2[0], point_2[1])),
            _point,
            tolerance=0.5,
        ):
            # print("CALLED") cv2.line(frame.frame, point_1, point_2, color=color, thickness=3)
            return True

    return False


def place_mid_points(frame: Frame):
    color = (255, 0, 0)
    radius = 5

    for point in frame.all_mid_points():
        if is_point_on_line(frame.line, point, tolerance=0.5):
            cv2.circle(
                frame.frame,
                point.get_vectors(),
                radius,
                color=(125, 125, 125),
                thickness=-1,
            )
            cv2.line(
                frame.frame,
                frame.line.point_1.get_vectors(),
                frame.line.point_2.get_vectors(),
                color=(0, 0, 255),
                thickness=3,
            )
        else:
            cv2.circle(frame.frame, point.get_vectors(), radius, color, thickness=-1)
    # for box in frame.obj_list:
    #     _mid_point = mid_point(box["box_points"])
    #     _point = Point(_mid_point[0], _mid_point[1])
    #     if is_point_on_line(
    #         Line(Point(point_1[0], point_1[1]), Point(point_2[0], point_2[1])),
    #         _point,
    #         tolerance=0.5,
    #     ):
    #         # print("CALLED")
    #         cv2.line(frame.frame, point_1, point_2, color=color, thickness=3)
    #
    #     cv2.circle(frame.frame, _mid_point, 5, color=color, thickness=-1)


def is_infringed(frame: Frame, point_1: tuple, point_2: tuple):
    for box in frame.obj_list:
        _mid_point = mid_point(box["box_points"])
        _point = Point(_mid_point[0], _mid_point[1])
        if is_point_on_line(
            Line(Point(point_1[0], point_1[1]), Point(point_2[0], point_2[1])),
            _point,
            tolerance=0.5,
        ):
            # print("CALLED")
            pass


def delete_files_in_folder(folder_path: Path):
    files = folder_path.glob("*.jpeg")
    print("FLUSHING TEMP FOLDER DATA")
    for file in files:
        os.remove(file)
    print("FLUSHED TEMP FOLDER")


def main():
    url: Path = Path(r"C:\Users\smath\OneDrive\Desktop\sample videos\vid_2.mp4")
    de: DetectionEngine = DetectionEngine(url)

    objects = de.detect_objects_from_frames(Line(Point(0, 0), Point(100, 100)))

    print(objects)

if __name__ == "__main__":
    main()

#     output_url = 'datafiles'
#
#     coord = Line(Point(207, 219), Point(610, 211))
#     color = (128, 0, 128)
#
#     # F = (96, 369) S= (338, 366)
#
#     de: DetectionEngine = DetectionEngine(url, output_url, 24)
#     frames: list[Frame] = de.process_frames(line_coords=coord, save_location='')
#     print(frames)
#     CANVAS_WIDTH = 800
#     CANVAS_HEIGHT = 500
#
#     WIDTH = len(frames[0].frame[0][0])
#     HEIGHT = len(frames[0].frame[0])
#
#     coordinates1 = (int(coord.point_1.x), int(coord.point_1.y))
#     coordinates2 = (int(coord.point_2.x), int(coord.point_2.y))
#     print(coordinates1, coordinates2)
#
#     final_frames = []
#
#     for frame in frames:
#         cv2.line(frame.frame, coordinates1, coordinates2, color=color, thickness=3)
#
#         # cv2.circle(frame, (314, 232), 5, color=color, thickness=3)
#         # cv2.circle(frame, (340, 252), 5, color=color, thickness=3)
#         place_mid_points(frame, color=(0, 0, 255), radius=5, point_1=coordinates1, point_2=coordinates2)
#         # cv2.circle(frame.frame, mid_point(frame.obj_list[0]['box_points']), 1, color=color, thickness=3)
#
#
#         # cv2.circle(frame, (314, 232), 5, color=color, thickness=3)
#
#         final_frames.append(frame)
#         cv2.imshow("AI", frame.frame)
#         time.sleep(0.1)
#         cv2.waitKey(1)
#
#     DetectionEngine.convert_frames_to_video(final_frames, 'myVid.avi')
#
