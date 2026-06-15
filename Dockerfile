# Stage 1: Sử dụng một image Alpine nhỏ gọn có sẵn công cụ zip
FROM alpine:latest 

# Cài đặt công cụ zip
RUN apk add --no-cache zip

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép CHÍNH XÁC các file và thư mục bạn yêu cầu vào container
COPY .env* ./ 
COPY .venv/ ./.venv/
COPY tests/ ./tests/
COPY tests_BONUS/ ./tests_BONUS/
COPY conftest.py pytest.ini README.md requirements.txt web_detector.py ./

# Tiến hành nén toàn bộ các file trong thư mục /app thành file project.zip
RUN zip -r /Group16_Automation.zip .

