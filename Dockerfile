FROM python:3.9

ADD main.py .

RUN pip install bs4 requests time json os flask

CMD ["python","./main.py"]