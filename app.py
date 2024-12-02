from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import QuestionForm, PeriodForm
import os
from dotenv import load_dotenv
import csv
from werkzeug.utils import secure_filename
import google.generativeai as genai
import time
# Tải biến môi trường
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = "./uploads"

# Kết nối MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client["time_travel_quiz"]
questions_collection = db["questions"]
periods_collection = db["periods"]

# Cấu hình Google Generative AI
genai.configure(api_key="AIzaSyBehj08D28PJAQ336By_Yhyj1ACYhhYD08")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
)
chat_session = model.start_chat(history=[])

def generate_history_question(prompt):
    response = chat_session.send_message(prompt)
    return response.text

# Route: Trang chủ
@app.route("/")
def home():
    return render_template("index.html")

# Route: Thêm câu hỏi
@app.route("/upload", methods=["GET", "POST"])
def upload_question():
    form = QuestionForm()
    # Lấy danh sách thời kỳ từ MongoDB
    periods = list(periods_collection.find())
    form.period.choices = [(str(period["_id"]), period["name"]) for period in periods]
    
    if form.validate_on_submit():  # Kiểm tra form hợp lệ
        try:
            period_id = ObjectId(form.period.data)  # Chuyển period thành ObjectId
        except:
            flash("Thời kỳ không hợp lệ.", "error")
            return redirect(url_for("upload_question"))
        
        question_data = {
            "question": form.question.data,
            "options": {
                "A": form.option_a.data,
                "B": form.option_b.data,
                "C": form.option_c.data,
                "D": form.option_d.data,
            },
            "correct_option": form.correct_option.data,
            "period_id": period_id,  # Lưu ID thời kỳ
        }
        questions_collection.insert_one(question_data)
        flash("Câu hỏi đã được upload thành công!", "success")
        return redirect(url_for("view_questions"))
    
    return render_template("upload.html", form=form)

@app.route("/generate-questions", methods=["GET", "POST"])
def generate_questions():
    periods = list(periods_collection.find())
    if request.method == "POST":
        period_id = request.form.get("period_id")
        num_questions = int(request.form.get("num_questions", 0))

        if not period_id:
            flash("Vui lòng chọn thời kỳ.", "error")
            return redirect(request.url)

        if num_questions <= 0:
            flash("Số lượng câu hỏi phải lớn hơn 0.", "error")
            return redirect(request.url)

        input_prompt_template = """
        Hãy tạo một câu hỏi trắc nghiệm lịch sử bằng tiếng Việt.
        Câu hỏi cần rõ ràng, súc tích, có 4 đáp án (A, B, C, D) và chỉ có một đáp án đúng.
        Đảm bảo định dạng như sau:
        Câu hỏi: <nội dung câu hỏi>
        A: <đáp án A>
        B: <đáp án B>
        C: <đáp án C>
        D: <đáp án D>
        Đáp án đúng: <A/B/C/D>
        """

        # Tạo câu hỏi tự động
        for _ in range(num_questions):
            try:
                response = generate_history_question(input_prompt_template)
                lines = response.strip().split("\n")
                question = next((line.split("Câu hỏi:")[1].strip() for line in lines if "Câu hỏi:" in line), "Unknown")
                option_a = next((line.split("A:")[1].strip() for line in lines if "A:" in line), "Unknown")
                option_b = next((line.split("B:")[1].strip() for line in lines if "B:" in line), "Unknown")
                option_c = next((line.split("C:")[1].strip() for line in lines if "C:" in line), "Unknown")
                option_d = next((line.split("D:")[1].strip() for line in lines if "D:" in line), "Unknown")
                correct_answer = next((line.split("Đáp án đúng:")[1].strip() for line in lines if "Đáp án đúng:" in line), "Unknown")

                question_data = {
                    "question": question,
                    "options": {
                        "A": option_a,
                        "B": option_b,
                        "C": option_c,
                        "D": option_d,
                    },
                    "correct_option": correct_answer,
                    "period_id": ObjectId(period_id),
                }
                questions_collection.insert_one(question_data)
                print(f"Đã thêm câu hỏi: {question}")
            except Exception as e:
                print(f"Lỗi khi tạo câu hỏi: {str(e)}")
                continue

            # Tạm dừng giữa các câu hỏi
            time.sleep(1)

        flash(f"{num_questions} câu hỏi đã được tạo và thêm vào MongoDB.", "success")
        return redirect(url_for("view_questions"))

    return render_template("generate_questions.html", periods=periods)

# Route: Upload câu hỏi bằng CSV
@app.route("/upload-csv", methods=["GET", "POST"])
def upload_csv():
    periods = list(periods_collection.find())
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            flash("Vui lòng chọn file CSV.", "error")
            return redirect(request.url)

        file = request.files["file"]
        period_id = request.form.get("period_id")
        if not period_id:
            flash("Vui lòng chọn thời kỳ.", "error")
            return redirect(request.url)

        try:
            # Đọc file CSV trực tiếp từ file upload
            reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())

            # Kiểm tra các cột bắt buộc
            required_columns = [
                "question", "option_a", "option_b", "option_c", "option_d", "correct_answer"
            ]
            if not all(column in reader.fieldnames for column in required_columns):
                missing_columns = [col for col in required_columns if col not in reader.fieldnames]
                flash(f"Thiếu các cột sau trong file CSV: {', '.join(missing_columns)}", "error")
                return redirect(request.url)

            # Thêm từng dòng dữ liệu vào MongoDB
            for row in reader:
                question_data = {
                    "question": row["question"],
                    "options": {
                        "A": row["option_a"],
                        "B": row["option_b"],
                        "C": row["option_c"],
                        "D": row["option_d"],
                    },
                    "correct_option": row["correct_answer"],
                    "period_id": ObjectId(period_id),
                }
                questions_collection.insert_one(question_data)

            flash("Câu hỏi từ file CSV đã được upload thành công!", "success")
            return redirect(url_for("view_questions"))
        except Exception as e:
            flash(f"Lỗi trong quá trình xử lý file: {str(e)}", "error")
            return redirect(request.url)

    return render_template("upload_csv.html", periods=periods)

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
        question["_id"] = str(question["_id"])  # Chuyển ObjectId thành chuỗi
        question["period_id"] = str(question["period_id"])  # Chuyển ObjectId của period_id (nếu có)
        
        # Lấy tên thời kỳ
        period = periods_collection.find_one({"_id": ObjectId(question["period_id"])})
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
