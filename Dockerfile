# set a base environment
FROM python:3.7.10-slim
# We copy just the requirements.txt first to leverage Docker cache
COPY ./app/requirements.txt ./requirements.txt
# define local working directory (not in the container)
WORKDIR /app
# install the dependencies
RUN pip3 install -r requirements.txt
# copy the contents of working directory into an /app folder (which is created if does not exist) in the container
COPY . /app
# run flask app from the app.py file inside the just created /app folder
CMD ["python","/app/app.py"]
