from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class QuestionForm(FlaskForm):
    period = SelectField("Thời kỳ", choices=[], validators=[DataRequired()])
    question = TextAreaField("Câu hỏi", validators=[DataRequired(), Length(min=10)])
    option_a = StringField("Đáp án A", validators=[DataRequired()])
    option_b = StringField("Đáp án B", validators=[DataRequired()])
    option_c = StringField("Đáp án C", validators=[DataRequired()])
    option_d = StringField("Đáp án D", validators=[DataRequired()])
    correct_option = SelectField(
        "Đáp án đúng",
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Thêm câu hỏi")


class PeriodForm(FlaskForm):
    name = StringField("Tên thời kỳ", validators=[DataRequired()])
    submit = SubmitField("Thêm Thời Kỳ")
