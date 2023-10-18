# use a python 3.8 base image
FROM python:3.8

# set the working directory to /app
WORKDIR /app

# copy all the files from the app directory to the container working directory
COPY /app /app

# Install packages defined in the requirements.txt file
RUN pip install -r requirements.txt
# Generate gRPC files
RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto

# expose the port 5005
EXPOSE 5005

# execute the techtrends application
CMD ["python", "main.py"]