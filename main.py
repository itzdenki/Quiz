from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QStackedWidget, QLineEdit, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer
import sys
import requests
import random

# URL của API để lấy dữ liệu câu hỏi
API_URL = "http://127.0.0.1:5000/api/questions"

# Hàm lấy dữ liệu câu hỏi từ API
def fetch_questions():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        questions = data.get("questions", [])
        return random.sample(questions, min(10, len(questions)))
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Không thể tải câu hỏi từ API.\nChi tiết: {str(e)}")
        return []

# Lớp giao diện chính của ứng dụng
class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quiz Lịch Sử")
        self.setGeometry(100, 100, 900, 700)

        self.questions = fetch_questions()
        self.current_question = None
        self.score = 0
        self.question_index = 0
        self.timer = None
        self.time_left = 10
        self.username = ""

        # Thiết lập font
        font = QFont("Arial", 14)
        self.setFont(font)

        # Quản lý các màn hình với QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Màn hình nhập username
        self.username_screen = self.create_username_screen()
        self.stacked_widget.addWidget(self.username_screen)

        # Màn hình hướng dẫn
        self.instructions_screen = self.create_instructions_screen()
        self.stacked_widget.addWidget(self.instructions_screen)

        # Màn hình quiz
        self.quiz_screen = self.create_quiz_screen()
        self.stacked_widget.addWidget(self.quiz_screen)

        # Hiển thị màn hình nhập username
        self.stacked_widget.setCurrentWidget(self.username_screen)

    def create_username_screen(self):
        username_screen = QWidget()
        username_layout = QVBoxLayout()
        username_layout.setContentsMargins(50, 50, 50, 50)

        title_label = QLabel("Quiz Lịch Sử")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #1E88E5;")
        username_layout.addWidget(title_label)

        username_input_label = QLabel("Nhập tên của bạn:")
        username_input_label.setStyleSheet("font-size: 18px; color: #555;")
        username_layout.addWidget(username_input_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tên...")
        self.username_input.setStyleSheet("""
            font-size: 16px; padding: 10px; border: 2px solid #1E88E5; border-radius: 5px;
        """)
        username_layout.addWidget(self.username_input)

        username_submit_button = QPushButton("Tiếp tục")
        username_submit_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        username_submit_button.clicked.connect(self.submit_username)
        username_layout.addWidget(username_submit_button)

        username_screen.setLayout(username_layout)
        return username_screen

    def create_instructions_screen(self):
        instructions_screen = QWidget()
        instructions_layout = QVBoxLayout()
        instructions_layout.setContentsMargins(50, 50, 50, 50)

        instructions_label = QLabel("Hướng dẫn chơi")
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF6F00;")
        instructions_layout.addWidget(instructions_label)

        instructions_detail = QLabel(
            "1. Mỗi câu hỏi có 4 đáp án, bạn chỉ có 10 giây để trả lời.\n"
            "2. Trả lời đúng sẽ được 1 điểm, trả lời sai hoặc hết thời gian sẽ không được điểm.\n"
            "3. Bạn có thể quay lại màn hình chính sau khi hoàn thành quiz.\n\n"
            "Nhấn 'Bắt đầu' để vào phần chơi."
        )
        instructions_detail.setStyleSheet("font-size: 16px; color: #333;")
        instructions_detail.setAlignment(Qt.AlignLeft)
        instructions_detail.setWordWrap(True)
        instructions_layout.addWidget(instructions_detail)

        start_quiz_button = QPushButton("Bắt đầu")
        start_quiz_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #FF6F00;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E65100;
            }
        """)
        start_quiz_button.clicked.connect(self.start_quiz)
        instructions_layout.addWidget(start_quiz_button)

        instructions_screen.setLayout(instructions_layout)
        return instructions_screen

    def create_quiz_screen(self):
        quiz_screen = QWidget()
        quiz_layout = QVBoxLayout()
        quiz_layout.setContentsMargins(50, 50, 50, 50)

        self.header_label = QLabel("")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 18px; color: #333;")
        quiz_layout.addWidget(self.header_label)

        self.timer_label = QLabel("Thời gian: 10 giây")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 18px; color: #F44336;")
        quiz_layout.addWidget(self.timer_label)

        self.question_label = QLabel("")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("font-size: 24px; color: #333; padding: 20px;")
        self.question_label.setWordWrap(True)
        quiz_layout.addWidget(self.question_label)

        self.answer_buttons = []
        for i in range(4):
            btn = QPushButton("")
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 15px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:disabled {
                    background-color: #bdbdbd;
                    color: #f4f4f4;
                }
            """)
            btn.clicked.connect(self.check_answer)
            quiz_layout.addWidget(btn)
            self.answer_buttons.append(btn)

        self.back_button = QPushButton("Quay lại màn hình chính")
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        self.back_button.clicked.connect(self.reset_to_username_screen)
        self.back_button.hide()
        quiz_layout.addWidget(self.back_button)

        quiz_screen.setLayout(quiz_layout)
        return quiz_screen

    def submit_username(self):
        self.username = self.username_input.text().strip()
        if not self.username:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên của bạn!")
            return
        self.stacked_widget.setCurrentWidget(self.instructions_screen)

    def start_quiz(self):
        self.header_label.setText(f"Người chơi: {self.username} | Điểm: {self.score}")
        self.stacked_widget.setCurrentWidget(self.quiz_screen)
        self.show_question()

    def reset_to_username_screen(self):
        self.questions = fetch_questions()
        self.current_question = None
        self.score = 0
        self.question_index = 0
        self.username_input.clear()
        self.stacked_widget.setCurrentWidget(self.username_screen)

    def show_question(self):
        if self.question_index < len(self.questions):
            self.current_question = self.questions[self.question_index]
            self.question_label.setText(f"Câu hỏi {self.question_index + 1}: {self.current_question['question']}")

            options = [
                self.current_question["options"]["A"],
                self.current_question["options"]["B"],
                self.current_question["options"]["C"],
                self.current_question["options"]["D"],
            ]
            random.shuffle(options)
            for i, btn in enumerate(self.answer_buttons):
                btn.setText(options[i])
                btn.setEnabled(True)

            self.start_timer()
        else:
            self.show_completion_screen()

    def check_answer(self):
        sender = self.sender()
        selected_option = sender.text()
        correct_option = self.current_question["options"][self.current_question["correct_option"]]

        self.timer.stop()
        if selected_option == correct_option:
            # Tính điểm dựa trên thời gian còn lại
            points_for_question = int(self.time_left * 10 / 10)  # Thời gian còn lại x 10 điểm
            self.score += points_for_question
            self.header_label.setText(f"Người chơi: {self.username} | Điểm: {self.score}")
            self.show_popup(f"Chính xác! Bạn nhận được {points_for_question} điểm.", "#4CAF50")
        else:
            self.show_popup(f"Sai! Đáp án đúng: {correct_option}", "#FF5722")

        for btn in self.answer_buttons:
            btn.setEnabled(False)

        QTimer.singleShot(2000, self.next_question)

    def start_timer(self):
        self.time_left = 10
        self.update_timer()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.countdown)
        self.timer.start(1000)

    def countdown(self):
        self.time_left -= 1
        self.update_timer()
        if self.time_left <= 0:
            self.timer.stop()
            correct_option = self.current_question["options"][self.current_question["correct_option"]]
            self.show_popup(f"Hết thời gian! Đáp án đúng: {correct_option}", "#FF5722")
            QTimer.singleShot(2000, self.next_question)

    def update_timer(self):
        self.timer_label.setText(f"Thời gian: {self.time_left} giây")

    def show_popup(self, message, color):
        self.question_label.setStyleSheet(f"background-color: {color}; color: white; font-size: 24px; padding: 20px;")
        self.question_label.setText(message)
        QTimer.singleShot(1500, self.reset_popup)

    def reset_popup(self):
        self.question_label.setStyleSheet("font-size: 24px; color: #333; padding: 20px;")

    def next_question(self):
        self.question_index += 1
        self.show_question()

    def show_completion_screen(self):
        self.question_label.setText(f"Bạn đã hoàn thành bài quiz!\nĐiểm số: {self.score}/100")
        for btn in self.answer_buttons:
            btn.hide()
        self.back_button.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec())
