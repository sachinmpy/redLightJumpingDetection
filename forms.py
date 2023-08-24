import logging
from flask_wtf import FlaskForm
from wtforms import DateField, FileField, TimeField
from wtforms.validators import InputRequired

logger = logging.getLogger(__name__)


class SpecificDateForm(FlaskForm):
    datefield = DateField()


class SpecificDateRangeForm(FlaskForm):
    start_date = DateField()
    end_date = DateField()


class VideoUploadForm(FlaskForm):
    # file_import = FileField(validators=[InputRequired()])
    # file_date = DateField(validators=[InputRequired()])
    # file_time = TimeField(validators=[InputRequired()])

    file_import = FileField()
    file_date = DateField()
    file_time = TimeField()

