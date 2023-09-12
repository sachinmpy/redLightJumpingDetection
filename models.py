
# Model Part of the pattern

import logging

logger = logging.getLogger(__name__)


class BaseModel:
    pass


class Video:

    VIDEO_PATH: str

    def __init__(self, file_name: str, meta_data: dict):
        self.file_name = file_name
        self.meta_data = meta_data

    def video_format(self, file_name: str):
        pass


class Frame:

    def __init__(self):
        pass

