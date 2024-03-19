FROM python:3.10 AS build 
USER root
ADD /app /app
RUN pip3 install -r /app/requirements.txt -t /python-env


ENV PYTHONPATH=/python-env
WORKDIR /app
CMD ["python3", "main.py"]
