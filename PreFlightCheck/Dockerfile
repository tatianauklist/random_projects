FROM python:3.11-slim

LABEL authors="tatianauklist"
LABEL description="Weekly report automation script"


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY logic/ ./logic/
COPY main.py .

CMD ["python3","main.py"]