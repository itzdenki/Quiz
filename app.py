from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import FileField, SelectField, SubmitField
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os
import docx
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Tải biến môi trường từ .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") 
csrf = CSRFProtect(app)

# Kết nối MongoDB
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["time_travel_quiz"]  # Cơ sở dữ liệu
questions_collection = db["questions"]
periods_collection = db["periods"]

# Đường dẫn lưu file tải lên
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"docx"}

# Trang chủ
@app.route("/")
def home():
    return render_template("index.html")

# Flask-WTF form class
class UploadDocxForm(FlaskForm):
    file = FileField("Chọn file .docx")
    period_id = SelectField("Chọn Thời Kỳ", coerce=str)
    submit = SubmitField("Tải lên")

# Hàm đọc câu hỏi từ file .docx
def parse_docx(file_path):
    doc = docx.Document(file_path)
    questions = []
    
    question = None  # Biến tạm để chứa câu hỏi
    options = []  # Biến lưu các đáp án

    for para in doc.paragraphs:
        text = para.text.strip()
        
        # Kiểm tra nếu đoạn văn bắt đầu bằng "Câu"
        if text.startswith("Câu") and question is not None:
            # Nếu câu hỏi trước đó đã có, lưu câu hỏi và đáp án vào danh sách
            questions.append({
                "question": question,
                "options": options
            })
            options = []  # Reset đáp án
            question = text  # Cập nhật câu hỏi mới
        elif text.startswith("Câu"):
            # Cập nhật câu hỏi khi bắt đầu bằng "Câu"
            question = text
        elif text.startswith("A.") or text.startswith("B.") or text.startswith("C.") or text.startswith("D."):
            # Loại bỏ các ký tự như "A.", "B." và thêm đáp án vào danh sách options
            option = text.split(". ", 1)[1]  # Loại bỏ phần chữ cái A, B, C, D
            options.append(option)

    # Thêm câu hỏi cuối cùng sau khi duyệt hết các đoạn văn
    if question is not None:
        questions.append({
            "question": question,
            "options": options
        })
    
    return questions

# Trang upload câu hỏi từ file .docx
@app.route("/upload-docx", methods=["GET", "POST"])
def upload_docx():
    periods = list(periods_collection.find())  # Lấy danh sách thời kỳ từ MongoDB
    form = UploadDocxForm()

    # Cập nhật các options của SelectField
    form.period_id.choices = [(str(period["_id"]), period["name"]) for period in periods]

    if form.validate_on_submit():
        file = form.file.data
        period_id = form.period_id.data  # Lấy thời kỳ được chọn

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            
            # Đọc câu hỏi từ file
            questions = parse_docx(file_path)

            # Hiển thị câu hỏi với nút Thêm
            return render_template("upload_docx.html", form=form, questions=questions, periods=periods)

    # Nếu không có POST, chỉ hiện form tải lên
    return render_template("upload_docx.html", form=form, periods=periods)

# Kiểm tra định dạng file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['docx']

# Upload câu hỏi
@app.route("/upload", methods=["GET", "POST"])
def upload_question():
    form = QuestionForm()
    if form.validate_on_submit():
        # Lấy thông tin từ form
        question_data = {
            "question": form.question.data,
            "options": {
                "A": form.option_a.data,
                "B": form.option_b.data,
                "C": form.option_c.data,
                "D": form.option_d.data,
            },
            "correct_option": form.correct_option.data,
            "period_id": ObjectId(form.period.data)  # Lưu ID của thời kỳ
        }
        # Lưu câu hỏi vào MongoDB
        questions_collection.insert_one(question_data)
        return redirect(url_for("view_questions"))
    # Lấy danh sách thời kỳ từ MongoDB
    periods = list(periods_collection.find())
    return render_template("upload.html", form=form, periods=periods)

# Hiện câu hỏi
@app.route("/view-questions")
def view_questions():
    questions = list(questions_collection.find())
    for question in questions:
        question["_id"] = str(question["_id"])
        if "period_id" in question:
            period = periods_collection.find_one({"_id": question["period_id"]})
            question["period_name"] = period["name"] if period else "Không xác định"
        else:
            question["period_name"] = "Không xác định"
    return render_template("view_questions.html", questions=questions)

# Xóa câu hỏi
@app.route("/delete-question/<question_id>", methods=["GET", "POST"])
def delete_question(question_id):
    questions_collection.delete_one({"_id": ObjectId(question_id)})
    return redirect(url_for("view_questions"))

# Quản lý thời kỳ
@app.route("/manage-periods", methods=["GET", "POST"])
def manage_periods():
    form = PeriodForm()
    if form.validate_on_submit():
        periods_collection.insert_one({"name": form.name.data})
        return redirect(url_for("manage_periods"))

    periods = list(periods_collection.find())
    for period in periods:
        period["_id"] = str(period["_id"])
    return render_template("periods.html", form=form, periods=periods)

# Xóa thời kỳ
@app.route("/delete-period/<period_id>", methods=["GET", "POST"])
def delete_period(period_id):
    period = periods_collection.find_one({"_id": ObjectId(period_id)})
    if period:
        questions_collection.update_many(
            {"period_id": ObjectId(period_id)},
            {"$unset": {"period_id": ""}}  # Xóa thời kỳ khỏi câu hỏi
        )
        periods_collection.delete_one({"_id": ObjectId(period_id)})
    
    return redirect(url_for("view_periods"))

# Xem thời kỳ
@app.route("/view-periods")
def view_periods():
    periods = list(periods_collection.find())
    return render_template("view_periods.html", periods=periods)

# API lấy danh sách câu hỏi
@app.route("/questions", methods=["GET"])
def get_questions():
    questions = list(questions_collection.find())
    for question in questions:
        question["_id"] = str(question["_id"])
    return jsonify(questions)

# API lấy danh sách thời kỳ
@app.route("/periods", methods=["GET"])
def get_periods():
    periods = list(periods_collection.find())
    for period in periods:
        period["_id"] = str(period["_id"])
    return jsonify(periods)

if __name__ == "__main__":
    app.run(debug=True)
