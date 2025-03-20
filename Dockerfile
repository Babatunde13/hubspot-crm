FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4012

CMD ["sh", "-c", "flask db upgrade && python run.py"]

