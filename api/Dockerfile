FROM python:3.10

COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Expose the required port
EXPOSE 8080

#Run the command
CMD gunicorn main:app