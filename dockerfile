FROM python:3.9

#  

EXPOSE 8000

WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

COPY ./app/config.faraday.json /code/config.faraday.json

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]