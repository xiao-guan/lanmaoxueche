FROM python:3.9

COPY requirements.txt requirements.txt

# 安装requests依赖
RUN pip install -r requirements.txt
