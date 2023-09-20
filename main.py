import logging
import os
import cv2

from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from tools.detectionengine import Point, Line, Frame, DetectionEngine
from tools.videoprocessing import Video
from databaseHandler import RljdDBHandler
from pathlib import Path
from forms import (
    SpecificDateForm,
    SpecificDateRangeForm,
    VideoUploadForm,
    CoordinatesForm,
)

# settings
from settings import TEMP_FRAMES, TEMP_IMAGES, VIDEO_DIR, FINAL_VID
from settings import DBSettings


# Flask Settings
app = Flask(__name__, static_url_path="/static")
app.config["SECRET_KEY"] = "ksdjfalkasjws22KSJDLKa"

UPLOAD_FOLDER = "videofiles/unhandled"
IMAGE_FOLDER = "static/unhandled_images"


# Logging and Env variables
# TODO: Create logging config file
logging.basicConfig(
    level=logging.DEBUG,
    format=" [ %(levelname)s ] - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Database
db: RljdDBHandler = RljdDBHandler(DBSettings, "infringement")


# Flask views
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/control-panel")
def control_panel():
    return render_template("control_panel.html")


@app.route("/review-media")
def review_media():
    try:
        file_uploaded: bool = (
            False if request.args["file_uploaded"] == "" else True
        )  # TODO: Find better way to handle
        image_url: str = "/static/images/image_1.jpg"
    except KeyError:
        file_uploaded = False
        image_url = ""

    logger.debug(f"Bool: {request.args}")
    video_form: VideoUploadForm = VideoUploadForm()
    logger.debug(file_uploaded)
    return render_template(
        "review_media.html",
        video_form=video_form,
        file_uploaded=file_uploaded,
        image_url=image_url,
    )


@app.route("/review-media/edit/<file_metadata>", methods=["GET", "POST"])
def edit_media(file_metadata: str):
    parse_metadata = file_metadata.split(",")
    hidden_form = CoordinatesForm()

    metadata = {
        "file_name": parse_metadata[0],
        "file_date": parse_metadata[1],
        "file_time": parse_metadata[2],
    }
    video_url = Path.joinpath(VIDEO_DIR, metadata["file_name"])
    video: Video = Video(video_url)

    metadata["first_frame"] = Video.save_as_image(
        video.get_first_frame(), TEMP_IMAGES, metadata['file_name']
    )
    image_url = metadata["first_frame"]

    return render_template(
        'edit_file.html',
        image_url=image_url,
        file_metadata=file_metadata,
        hidden_form=hidden_form,
    )


@app.route("/review-media/processing/<file_metadata>", methods=["POST"])
def processing(file_metadata):
    parsed_data = file_metadata.split(",")
    metadata = {
        "file_name": parsed_data[0],
        "file_date": parsed_data[1],
        "file_time": parsed_data[2],
        "f_coords": tuple(request.form["first_coords"].split(",")),
        "s_coords": tuple(request.form["second_coords"].split(",")),
    }

    p1 = Point(int(metadata["f_coords"][0]), int(metadata["f_coords"][1]))
    p2 = Point(int(metadata["s_coords"][0]), int(metadata["s_coords"][1]))

    print(metadata["file_name"])

    de: DetectionEngine = DetectionEngine(
        Path(
            rf"C:\Users\smath\PycharmProjects\redLightJumpingDetection\videofiles\unhandled\{metadata['file_name']}"
        ),
        Path(""),
        24,
    )
    line: Line = Line(p1, p2)
    frames: list[Frame] = de.process_frames(line, "")
    de.construct_video(frames)
    de.write_to_db(
        frames, metadata["file_name"], metadata["file_date"], metadata["file_time"]
    )

    logger.debug(metadata)

    return render_template("processing_final.html", metadata=metadata)


@app.route("/generate-report")
def generate_report():
    specific_date_form = SpecificDateForm()
    date_range_form = SpecificDateRangeForm()
    return render_template(
        "generate_report.html", sd_form=specific_date_form, dr_form=date_range_form
    )


@app.route("/generate-report/generate-specific-day-report/", methods=["POST", "GET"])
def generate_specific_date_report():
    # form: SpecificDateForm = SpecificDateForm()  # TODO: To be removed
    date = request.form["datefield"]
    if date:
        q = {
            "file_date": date,
        }
        cursor = db.query(q)

        total_infringements = 0
        for record in cursor:
            total_infringements += 1
            logger.debug(record)

        report_string = f"{date}"
        return render_template(
            "report.html",
            total_infringements=total_infringements,
            report_string=report_string,
        )

    # if form.validate():
    logger.debug(request.form["datefield"])
    return redirect(url_for("generate_report"))


@app.route(
    "/generate-report/generate-specific-day-range-report/", methods=["POST", "GET"]
)
def generate_specific_date_range_report():
    # form: SpecificDateRangeForm = SpecificDateRangeForm()
    start = request.form["start_date"]
    end = request.form["end_date"]

    if start and end:
        q = {"file_date": {"$gte": start, "$lte": end}}
        cursor = db.query(q)

        total_infringements = 0
        for record in cursor:
            total_infringements += 1

        report_string = f"{start} - {end}"

        return render_template(
            "report.html",
            total_infringements=total_infringements,
            report_string=report_string,
        )

    logger.debug(request.form["start_date"])
    logger.debug(request.form["end_date"])

    return redirect(url_for("generate_report"))


@app.route("/review-media/upload-video", methods=["POST", "GET"])
def get_uploaded_video():
    uploaded_video: VideoUploadForm = VideoUploadForm()
    if request.method == "POST" and "file_import" in request.files:
        file_metadata = {
            "file_date": request.form["file_date"],
            "file_time": request.form["file_time"],
        }
        file = request.files["file_import"]
        file_name = secure_filename(file.filename)
        file_metadata["file_name"] = file_name
        metadata = f"{file_metadata['file_name']},{file_metadata['file_date']},{file_metadata['file_time']}"
        os.chdir(
            "C:\\Users\\smath\\PycharmProjects\\redLightJumpingDetection"
        )  # TODO: make it dynamic

        if not os.path.exists(UPLOAD_FOLDER + "/" + file_name):
            try:
                file.save(UPLOAD_FOLDER + "/" + file_name)

            except FileNotFoundError:
                logger.debug("_________ FILE NOT FOUND _____________")
                return redirect((url_for("review_media")))

        return redirect(url_for("edit_media", file_metadata=metadata))

    logger.debug(request.form)
    return redirect(url_for("review_media"))


if __name__ == "__main__":
    app.run(debug=True)
