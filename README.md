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

1. **Chạy ứng dụng**:
   - Sau khi hoàn tất cài đặt, khởi chạy ứng dụng bằng lệnh:
     ```bash
     python main.py
     ```
---

## **Thư viện sử dụng**
- **`requests`**: Lấy câu hỏi từ API.
- **`PySlide6`**: Làm APP
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
