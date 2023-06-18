FROM python:3.11.4

COPY ./requirements.txt /requirements.txt

RUN pip --default-timeout=1000 install --no-cache-dir --upgrade -r requirements.txt

COPY ./model /model/
COPY ./notebook /notebook/
COPY ./code /code/
COPY ./data /data/

WORKDIR /code
CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]