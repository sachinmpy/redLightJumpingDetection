# Settings variables and enums goes here

import logging
import os

from pathlib import Path

logger = logging.getLogger(__name__)

# Project paths
BASE_DIR = Path(r'C:\Users\smath\PycharmProjects\redLightJumpingDetection')
TEMP_DIR = Path.joinpath(BASE_DIR, "temp_dir")  # Data in the folder will be flushed regularly

VIDEO_DIR = Path.joinpath(TEMP_DIR, 'videofiles')
IMAGE_DIR = Path.joinpath(TEMP_DIR, "imagefiles")

TEMP_FRAMES = Path.joinpath(IMAGE_DIR, "temp_frame")
TEMP_IMAGES = Path.joinpath(IMAGE_DIR, "temp_images")


# Database Settings
DBSettings: dict = {
    'host': "localhost",
    'port': 27017,
    'database': "red-light-jumping-detection",
    'collectionList': []
}

# User paths
# Final Video will be saved in this location
FINAL_VID = BASE_DIR


def main() -> None:
    pass


if __name__ == "__main__":
    main()
