FROM python:3.9

ADD main.py .

RUN pip install bs4 requests flask 
CMD ["python","./main.py"]