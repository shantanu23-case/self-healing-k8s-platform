FROM python:3.11

RUN pip install flask kubernetes

COPY ./healer/healer.py .

CMD ["python","healer.py"]