# set a base environment
FROM python:3.7.10-slim
# We copy just the requirements.txt first to leverage Docker cache
COPY ./app/requirements.txt ./app/requirements.txt
# define the working directory inside the container (created if does not exist)
WORKDIR /app
# install the dependencies
RUN pip3 install -r requirements.txt
# copy the contents of app/ external directory inside current container directory (app/):
COPY ./app .
# run flask app from the app.py file inside the just created /app folder
CMD ["python","app.py"]
