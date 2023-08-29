import logging
import os
import cv2

from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from tools.videoprocessing import Video

from forms import SpecificDateForm, SpecificDateRangeForm, VideoUploadForm

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = "ksdjfalkasjws22KSJDLKa"

UPLOAD_FOLDER = "videofiles/unhandled"

logging.basicConfig(level=logging.DEBUG, format=" [ %(levelname)s ] - %(name)s - %(message)s", )
logger = logging.getLogger(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/control-panel")
def control_panel():
    return render_template("control_panel.html")


@app.route("/review-media")
def review_media():
    try:
        file_uploaded: bool = False if request.args['file_uploaded'] == '' else True  # TODO: Find better way to handle
        image_url: str = "/static/images/image_1.jpg"
    except KeyError:
        file_uploaded = False
        image_url = ''

    logger.debug(f'Bool: {request.args}')
    video_form: VideoUploadForm = VideoUploadForm()
    logger.debug(file_uploaded)
    return render_template("review_media.html",
                           video_form=video_form,
                           file_uploaded=file_uploaded,
                           image_url=image_url
                           )


@app.route("/review-media/edit/<file_metadata>", methods=['GET', 'POST'])
def edit_media(file_metadata: dict):
    image_url: str = "/static/images/image_1.jpg"
    metadata = file_metadata
    file_url = UPLOAD_FOLDER + "/" + metadata["file_name"]

    # video: Video = Video(file_url)

    # metadata['first_frame'] = video.get_first_frame()
    logger.debug(metadata)
    return render_template("edit_file.html", image_url=image_url)


@app.route("/generate-report")
def generate_report():
    specific_date_form = SpecificDateForm()
    date_range_form = SpecificDateRangeForm()
    return render_template("generate_report.html",
                           sd_form=specific_date_form,
                           dr_form=date_range_form
                           )


@app.route("/generate-report/generate-specific-day-report/", methods=["POST", "GET"])
def generate_specific_date_report():
    form: SpecificDateForm = SpecificDateForm()
    # if form.validate():
    logger.debug(request.form["datefield"])
    return redirect(url_for('generate_report'))


@app.route("/generate-report/generate-specific-day-range-report/", methods=["POST", "GET"])
def generate_specific_date_range_report():
    # form: SpecificDateRangeForm = SpecificDateRangeForm()
    logger.debug(request.form["start_date"])
    logger.debug(request.form["end_date"])

    return redirect(url_for('generate_report'))


@app.route("/review-media/upload-video", methods=["POST", "GET"])
def get_uploaded_video():
    uploaded_video: VideoUploadForm = VideoUploadForm()
    if request.method == "POST" and 'file_import' in request.files:
        file_metadata = {
            "file_date": request.form['file_date'],
            "file_time": request.form['file_time'],
        }
        file = request.files['file_import']
        file_name = secure_filename(file.filename)
        file_metadata["file_name"] = file_name
        # file.save(os.path.join(UPLOAD_FOLDER, file_name))
        return edit_media(file_metadata=file_metadata)

    logger.debug(request.form)
    return redirect(url_for('review_media'))


if __name__ == '__main__':
    app.run(debug=True)
