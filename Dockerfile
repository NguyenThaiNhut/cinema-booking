FROM python:3.12
EXPOSE 8000
WORKDIR /member
COPY . /member/
RUN pip install -r requirements.txt
CMD python3 manage.py runserver 0.0.0.0:8000





# # Sử dụng image base có sẵn với Python và Django
# FROM python:3.12.1

# # Đặt biến môi trường để tránh hiện các thông báo không cần thiết
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV PYTHONUNBUFFERED 1

# # Tạo thư mục làm việc và di chuyển vào đó
# WORKDIR /src

# # Sao chép tất cả các file vào thư mục làm việc
# COPY . .

# # Cài đặt dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Chạy các lệnh migrate và collectstatic của Django
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# # Mở cổng 8000 để Django chạy
# EXPOSE 8000

# # Khởi chạy ứng dụng Django khi container được bật
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]