import cv2
import time
import os
import random
import logging

from numpy import ndarray

logger = logging.getLogger(__name__)


class Video:

    def __init__(self, url_path: str, metadata: dict) -> None:
        self.metadata = metadata
        self.url_path = url_path
        self.video_obj = cv2.VideoCapture(self.url_path)
        self.total_frames = self.video_obj.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video_obj.get(cv2.CAP_PROP_FPS)

    def read_frames(self, frame_count: int | None = None,
                    step: int = 1,
                    sleep_off: bool = False
                    ) -> list[ndarray]:
        frame_count = self.total_frames if frame_count is None else frame_count
        count, step_count = 0, 1

        frame_list = []
        # print("TOTAL FRAME", self.total_frames)
        while self.video_obj.isOpened() and count < frame_count:

            count += 1
            _, frame = self.video_obj.read()

            if _:

                if step_count != step:
                    step_count += 1
                    continue

                else:
                    step_count = 1

                time.sleep(1 / self.fps) if not sleep_off else time.sleep(0)
                frame_list.append(frame)
                # cv2.imshow('frame', frame)
                cv2.waitKey(1)

            else:
                break

        self.video_obj.release()
        cv2.destroyAllWindows()
        # print("STEPPED FRAME", len(frame_list))
        return frame_list

    def get_first_frame(self) -> ndarray:
        frame = self.read_frames(frame_count=1)[0]
        # cv2.imshow("My IMage", frame)
        # cv2.waitKey(1)
        return frame

    @staticmethod
    def save_to_image(frame: ndarray, folder_path: str, metadata: dict, extension: str = '.jpeg') -> None:
        try:
            os.chdir(folder_path)

        except FileNotFoundError as e:
            logger.error("FileNotFound, Path specified does not exist, check path and try again")
            return None

        filename = metadata['filename'] + "".join(random.choices("abcdefgh01234", k=4)) + extension
        cv2.imwrite(filename, frame)
        logger.info("File saved successfully")


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