FROM python:3.10.7
WORKDIR /code
COPY . .
RUN pip3 install --no-cache-dir -r /code/requirements.txt
CMD ["python3", "service/manage.py", "runserver", "0:8000"]