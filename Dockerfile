FROM python:latest
LABEL authors="Anton"
LABEL descriptor="TRSPO_05"

WORKDIR /opt/project
COPY . /opt/project

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6116

CMD ["python", "main.py"]
