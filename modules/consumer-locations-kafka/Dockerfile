# use a python 3.8 base image
FROM python:3.8

# set the working directory to /app
WORKDIR /app

# copy all the files from the consumer directory to the container working directory
COPY /app /app

# Install packages defined in the requirements.txt file
RUN pip install -r requirements.txt

# expose the port 5000
EXPOSE 5000

# execute the kafka consumer
CMD ["python", "consumer.py"]