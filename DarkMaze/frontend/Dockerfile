# TODO: Install the frontend dependency package into the app folder inside the container.
# 使用 Python 3.11 作為基礎映像
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製應用程式的 requirements.txt 到容器中
COPY requirements.txt /app/

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼到容器中
COPY . /app/

# 安裝前端依賴 (若有必要的話，可以在此處安裝前端依賴)
# RUN npm install (如果你有前端的 package.json，並且有 Node.js 依賴)

# 對外開放端口
EXPOSE 8088

# 設定容器啟動時執行的命令
CMD ["uvicorn", "src.template.backend.main:app", "--host", "0.0.0.0", "--port", "8088", "--reload"]
