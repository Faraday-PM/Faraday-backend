FROM python:3.9

#  

EXPOSE 8000

WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

ENV FARADAY_DATABASE_URL="INSERT URL HERE"
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]