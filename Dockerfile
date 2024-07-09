FROM python:3.10-slim

# https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx file for rembg
COPY u2net.onnx /root/.u2net/u2net.onnx

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
