# set conda as base environment
FROM continuumio/miniconda3

# make docker use bash instead of sh
SHELL ["/bin/bash","--login","-c"]

# We copy just the requirements.txt first to leverage Docker cache
COPY ./app/environment_web.yml /app/environment_web.yml
# Copy the module inside the root folder so that the container can use it
COPY ./lmpm /lmpm
# define the working directory inside the container (created if does not exist)
# we run from the root folder so that we find both the app and the library
#WORKDIR /app

# copy the contents of app/ external directory inside current container directory (app/):
COPY ./app /app

# make the entrypoint script executable
RUN chmod u+x /app/entrypoint.sh

# install the dependencies
#RUN pip3 install -r requirements.txt
# to run conda you have to do it this way:
RUN conda env create -f /app/environment_web.yml
# run entrypoint, so that conda is activated when running the CMD command and we effectively inside the conda environment
ENTRYPOINT ["/app/entrypoint.sh"]

# run flask app from the app.py file inside the just created /app folder
CMD ["python","/app/app.py"]
