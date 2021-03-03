# set a base environment
FROM python:3.7.10-slim
# We copy just the requirements.txt first to leverage Docker cache
COPY .app/app/requirements.txt /app/requirements.txt
# define working directory
WORKDIR /app
# install the dependencies
RUN pip3 install -r requirements.txt
# copy the working directory into an /app folder in the container
COPY . /app/app
# run flask app
CMD ["python","app/app.py"]
