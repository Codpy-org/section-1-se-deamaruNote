# 使用 Python 3.11 作為基礎映像
FROM python:3.11

# 設定容器內的工作目錄
WORKDIR /app

# 複製 Python 依賴文件到容器中
COPY requirements.txt /app/

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個應用程式代碼到容器內
COPY . /app/

# 設定容器啟動時執行的命令
CMD ["uvicorn", "src.template.backend.main:app", "--host", "0.0.0.0", "--port", "8088", "--reload"]
