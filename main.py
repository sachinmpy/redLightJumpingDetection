import logging
from flask import Flask, render_template, url_for, request, redirect

from forms import SpecificDateForm, SpecificDateRangeForm, VideoUploadForm

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = "ksdjfalkasjws22KSJDLKa"

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
        file_uploaded: bool = False if request.args['file_uploaded'] == '' else True
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
    logger.debug(request.form)
    return redirect(url_for('review_media', file_uploaded=True))


if __name__ == '__main__':
    app.run(debug=True)
