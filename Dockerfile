# set python as base environment
FROM python:3.8.8-slim

# We copy just the requirements.txt first to leverage Docker cache
COPY ./app/requirements.txt /app/requirements.txt

# To leverage cache we first install the requirements, which do not change as easily as lmpm or app
RUN pip3 install --no-cache-dir --compile -r /app/requirements.txt

# Copy the module inside the root folder so that the container can use it
COPY ./lmpm /lmpm
# define the working directory inside the container (created if does not exist)
# we run from the root folder so that we find both the app and the library
#WORKDIR /app

# copy the contents of app/ external directory inside current container directory (app/):
COPY ./app /app

# make the entrypoint script executable
#RUN chmod u+x /app/entrypoint.sh

# install the dependencies
#RUN pip3 install -r /app/requirements.txt
# to run conda you have to do it this way:
#RUN conda env create -f /app/environment_web.yml
# run entrypoint, so that conda is activated when running the CMD command and we effectively inside the conda environment
#ENTRYPOINT ["/app/entrypoint.sh"]

# run flask app from the app.py file inside the just created /app folder
CMD ["python","/app/app.py"]
