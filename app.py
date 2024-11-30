from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import QuestionForm, PeriodForm
import os
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Kết nối MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client["time_travel_quiz"]
questions_collection = db["questions"]
periods_collection = db["periods"]

# Route: Trang chủ
@app.route("/")
def home():
    return render_template("index.html")

# Route: Thêm câu hỏi
@app.route("/upload", methods=["GET", "POST"])
def upload_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question_data = {
            "question": form.question.data,
            "options": {
                "A": form.option_a.data,
                "B": form.option_b.data,
                "C": form.option_c.data,
                "D": form.option_d.data,
            },
            "correct_option": form.correct_option.data,
            "period_id": ObjectId(form.period.data),
        }
        questions_collection.insert_one(question_data)
        flash("Câu hỏi đã được upload thành công!", "success")  # Thông báo thành công
        return redirect(url_for("view_questions"))
    periods = list(periods_collection.find())
    form.period.choices = [(str(period["_id"]), period["name"]) for period in periods]
    return render_template("upload.html", form=form)

# Route: Xem câu hỏi
@app.route("/view-questions")
def view_questions():
    questions = list(questions_collection.find())
    for question in questions:
        question["_id"] = str(question["_id"])
        period = periods_collection.find_one({"_id": question.get("period_id")})
        question["period_name"] = period["name"] if period else "Không xác định"
    return render_template("view_questions.html", questions=questions)

# Route: Xóa câu hỏi
@app.route("/delete-question/<id>", methods=["POST"])
def delete_question(id):
    try:
        result = questions_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return redirect(url_for("view_questions"))
        else:
            return "Câu hỏi không tồn tại", 404
    except Exception as e:
        return f"Lỗi: {str(e)}", 500

# Route: Quản lý thời kỳ
@app.route("/manage-periods", methods=["GET", "POST"])
def manage_periods():
    form = PeriodForm()
    if form.validate_on_submit():
        period_data = {"name": form.name.data}
        periods_collection.insert_one(period_data)
        return redirect(url_for("manage_periods"))
    periods = list(periods_collection.find())
    for period in periods:
        period["_id"] = str(period["_id"])
    return render_template("periods.html", form=form, periods=periods)

# Route: Xóa thời kỳ
@app.route("/delete-period/<id>", methods=["POST"])
def delete_period(id):
    try:
        questions_collection.delete_many({"period_id": ObjectId(id)})
        result = periods_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return redirect(url_for("manage_periods"))
        else:
            return "Thời kỳ không tồn tại", 404
    except Exception as e:
        return f"Lỗi: {str(e)}", 500

# Route: Hiện thị câu hỏi JSON
@app.route("/api/questions", methods=["GET"])
def get_questions_json():
    questions = list(questions_collection.find())
    questions_json = []
    for question in questions:
        question["_id"] = str(question["_id"])  # Convert ObjectId to string
        period = periods_collection.find_one({"_id": question.get("period_id")})
        question["period_name"] = period["name"] if period else "Không xác định"
        questions_json.append(question)
    return {"questions": questions_json}, 200

# Route: Hiện thị thời kì JSON
@app.route("/api/periods", methods=["GET"])
def get_periods_json():
    periods = list(periods_collection.find())
    for period in periods:
        period["_id"] = str(period["_id"])  # Convert ObjectId to string
    return {"periods": periods}, 200

# Route: Câu hỏi + Thời kì JSON
@app.route("/api/data", methods=["GET"])
def get_all_data_json():
    # Lấy danh sách câu hỏi
    questions = list(questions_collection.find())
    questions_json = []
    for question in questions:
        question["_id"] = str(question["_id"])  # Convert ObjectId to string
        period = periods_collection.find_one({"_id": question.get("period_id")})
        question["period_name"] = period["name"] if period else "Không xác định"
        questions_json.append(question)

    # Lấy danh sách thời kỳ
    periods = list(periods_collection.find())
    for period in periods:
        period["_id"] = str(period["_id"])  # Convert ObjectId to string

    return {"questions": questions_json, "periods": periods}, 200


if __name__ == "__main__":
    app.run(debug=True)
