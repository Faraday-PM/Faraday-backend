FROM python:3.11

WORKDIR /faraday

COPY requirements.txt /faraday/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /faraday/requirements.txt

COPY / /faraday/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]