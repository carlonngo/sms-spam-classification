FROM python:3.11.4

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./model /model/

WORKDIR /code
COPY ./code /code/

CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]