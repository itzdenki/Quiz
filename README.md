# **Time Travel Quiz**

### **Mô tả sản phẩm**
Time Travel Quiz là một ứng dụng quản lý câu hỏi trắc nghiệm lịch sử. Ứng dụng hỗ trợ các giáo viên, học sinh, hoặc người đam mê lịch sử tạo, quản lý và học các câu hỏi về các thời kỳ lịch sử khác nhau. Ngoài ra, ứng dụng tích hợp API AI để tự động tạo câu hỏi lịch sử và cho phép upload dữ liệu hàng loạt thông qua file CSV.

---

## **Các tính năng chính**
1. **Thêm câu hỏi thủ công**: Tạo câu hỏi trắc nghiệm với các đáp án và thời kỳ liên quan.
2. **Xem danh sách câu hỏi**: Duyệt qua toàn bộ câu hỏi hiện có trong cơ sở dữ liệu.
3. **Quản lý thời kỳ**: Thêm, sửa hoặc xóa thời kỳ lịch sử.
4. **Upload câu hỏi từ file CSV**: Dễ dàng thêm nhiều câu hỏi cùng lúc. (đang bảo trì)
5. **Tạo câu hỏi tự động bằng AI**: Sử dụng Google Generative AI để tạo câu hỏi lịch sử tự động.
6. **API hỗ trợ**: Truy cập câu hỏi và thời kỳ dưới dạng JSON.

---

## **Vai trò của sản phẩm**
Time Travel Quiz giúp:
- **Giáo viên**: Quản lý câu hỏi dễ dàng để tạo bài kiểm tra hoặc bài tập lịch sử.
- **Học sinh**: Luyện tập và kiểm tra kiến thức lịch sử qua câu hỏi trắc nghiệm.
- **Người đam mê lịch sử**: Tìm hiểu thêm các thời kỳ lịch sử qua hình thức học tập thú vị.

---

## **Cách cài đặt**

### **1. Yêu cầu hệ thống**
- **Python**: 3.8 trở lên
- **MongoDB**: Cơ sở dữ liệu NoSQL để lưu trữ câu hỏi và thời kỳ
- **Pip**: Trình quản lý thư viện Python

---

### **2. Cài đặt**
1. **Clone hoặc tải mã nguồn về máy**:
   ```bash
   git clone https://github.com/itzdenki/Quiz.git
   cd Quiz
   ```

2. **Tạo môi trường ảo (virtual environment)**:
   Môi trường ảo giúp quản lý các thư viện Python mà không ảnh hưởng đến hệ thống toàn cục. Chạy lệnh sau để tạo môi trường ảo:

   ```bash
   python -m venv venv
   ```

3. **Kích hoạt môi trường ảo**:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Cài đặt thư viện yêu cầu**:
   Sau khi kích hoạt môi trường ảo, bạn cần cài đặt các thư viện yêu cầu trong file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```


## **Cách chạy ứng dụng**

1. **Khởi động MongoDB**:
   - Đảm bảo rằng MongoDB đã được cài đặt và đang chạy trên cổng mặc định (`localhost:27017`).
   - Nếu chưa cài đặt, bạn có thể tải và cài đặt MongoDB từ [trang chủ MongoDB](https://www.mongodb.com/try/download/community).
   - Sau khi cài đặt, khởi động MongoDB bằng lệnh:
     ```bash
     mongod
     ```

2. **Cấu hình file `.env`**:
   - Tạo file `.env` trong thư mục gốc của dự án và thêm nội dung sau:
     ```
     MONGO_URL=mongodb://localhost:27017/
     SECRET_KEY=your_secret_key_here
     api_key=ABCDXYZ
     ```
   - **MONGO_URL**: Địa chỉ kết nối MongoDB.
   - **SECRET_KEY**: Một chuỗi bất kỳ để bảo mật ứng dụng Flask.
   - **api_key**: API Key của Google Gemini.

3. **Chạy ứng dụng Flask**:
   - Sau khi hoàn tất cài đặt, khởi chạy ứng dụng bằng lệnh:
     ```bash
     python app.py
     ```

4. **Truy cập ứng dụng**:
   - Mở trình duyệt và truy cập:
     ```
     http://127.0.0.1:5000/
     ```

5. **Sử dụng API**:
   - **Xem danh sách câu hỏi** (dưới dạng JSON):
     ```
     http://127.0.0.1:5000/api/questions
     ```
   - **Xem danh sách thời kỳ** (dưới dạng JSON):
     ```
     http://127.0.0.1:5000/api/periods
     ```

---

## **Cách sử dụng**

### **1. Các chức năng chính**
- **Trang chủ**: Hiển thị danh sách các chức năng chính của ứng dụng.
- **Thêm câu hỏi**:
  - Chọn "Thêm câu hỏi thủ công" để nhập thông tin cho từng câu hỏi.
  - Nhập đầy đủ các trường: câu hỏi, các đáp án (A, B, C, D), đáp án đúng và thời kỳ liên quan.
- **Tạo câu hỏi tự động bằng AI**:
  - Chọn "Tạo câu hỏi tự động".
  - Chọn thời kỳ, nhập số lượng câu hỏi cần tạo, và ứng dụng sẽ tự động tạo câu hỏi dựa trên AI.
- **Upload câu hỏi từ file CSV**:
  - Chuẩn bị file CSV với cấu trúc sau:
    ```
    question,option_a,option_b,option_c,option_d,correct_answer
    ```
  - Truy cập "Upload câu hỏi từ file CSV", chọn thời kỳ và upload file.
- **Xem danh sách câu hỏi**:
  - Duyệt qua tất cả câu hỏi hiện có trong cơ sở dữ liệu.
  - Câu hỏi được hiển thị cùng với đáp án và thời kỳ.

---

## **Xử lý lỗi thường gặp**

1. **Không kết nối được MongoDB**:
   - Kiểm tra xem MongoDB đã được khởi chạy hay chưa:
     ```bash
     mongod
     ```
   - Nếu vẫn lỗi, kiểm tra cấu hình trong file `.env`:
     ```
     MONGO_URL=mongodb://localhost:27017/
     ```

2. **Lỗi không tìm thấy thư viện (`ModuleNotFoundError`)**:
   - Cài đặt thư viện bị thiếu bằng lệnh:
     ```bash
     pip install -r requirements.txt
     ```

3. **Lỗi khi upload CSV**:
   - Đảm bảo file CSV đúng định dạng và mã hóa UTF-8.
   - Kiểm tra tên các cột: `question, option_a, option_b, option_c, option_d, correct_answer`.

4. **Lỗi khi sử dụng API Google Generative AI**:
   - Đảm bảo bạn đã cài đặt thư viện:
     ```bash
     pip install google-generativeai
     ```
   - Kiểm tra API Key đã cấu hình trong file .env

---

## **Thư viện sử dụng**
- **`Flask`**: Framework xây dựng ứng dụng web.
- **`pymongo`**: Kết nối MongoDB với Python.
- **`google-generativeai`**: Tích hợp API Google Generative AI để tạo câu hỏi tự động.
- **`dotenv`**: Quản lý biến môi trường.
- **`csv`**: Xử lý file CSV để nhập/xuất dữ liệu.

---

## **Hỗ trợ**

Nếu bạn gặp lỗi hoặc cần hỗ trợ, vui lòng liên hệ:
- **Email**: itzdenki2007@gmail.com
---

## **Tác giả**
- **Tên**: Đỗ Huy Thịnh
- **Email**: itzdenki2007@gmail.com
- **GitHub**: [github.com/itzdenki](https://github.com/itzdenki)
- **Liên hệ**: Vui lòng gửi email hoặc tạo issue trên GitHub nếu bạn có bất kỳ câu hỏi nào.

---
