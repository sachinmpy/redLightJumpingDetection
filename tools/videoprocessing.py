import cv2
import time
import os
import random
import logging

import numpy
from numpy import ndarray
from pathlib import Path
logger = logging.getLogger(__name__)


class Video:

    def __init__(self, url_path: Path) -> None:
        self.url_path = url_path
        self.video_obj = cv2.VideoCapture(self.url_path.as_posix())
        self.TOTAL_FRAMES = self.video_obj.get(cv2.CAP_PROP_FRAME_COUNT)
        self.FPS = self.video_obj.get(cv2.CAP_PROP_FPS)

    def read_frames(self, frame_count: int | None = None,
                    step: int = 1,
                    ) -> list[ndarray]:
        frame_count = self.TOTAL_FRAMES if frame_count is None else frame_count
        count, step_count = 0, 1

        frame_list = []
        while self.video_obj.isOpened() and count < frame_count:
            count += 1
            _, frame = self.video_obj.read()

            if _:
                if step_count != step:
                    step_count += 1
                    continue

                else:
                    step_count = 1
                frame_list.append(cv2.resize(frame, (800, 500)))  # TODO: check this
                cv2.waitKey(1)

            else:
                break

        self.video_obj.release()
        cv2.destroyAllWindows()
        return frame_list

    def get_first_frame(self) -> ndarray:
        frame = self.read_frames(frame_count=1)[0]
        return frame

    @staticmethod
    def save_as_image(frame: ndarray, folder_path: str, file_name: str, extension: str = '.jpeg') -> str | None:
        filename = file_name + "".join(random.choices("abcdefgh01234", k=4)) + extension
        file_location = Path.joinpath(folder_path, filename)
        cv2.imwrite(file_location, frame)

        return file_location

if __name__ == "__main__":
    # url = "C:\\Users\\smath\\PycharmProjects\\redLightJumpingDetection\\videofiles\\unhandled\\bha.mp4"
    # folder_path = "C:\\Users\\smath\\PycharmProjects\\redLightJumpingDetection\\videofiles\\unhandled\\saved_frame"
    #
    # vid = Video(url, {})

    # while vid.isOpened():
    #     _, frame = vid.read()
    #     print(_)
    #     if _:
    #         time.sleep(1/24)
    #         cv2.imshow("frame", frame)
    #         if cv2.waitKey(1) & 0xFF:
    #             continue
    #     else:
    #         break

    # fframe = vid.get_first_frame()
    # Video.save_to_image(fframe, folder_path, {"filename": "myimage"})

    pass