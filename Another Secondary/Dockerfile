#Use the Python3.7.2 image
FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./ ./

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
#CMD ["uwsgi", "app.ini", "flask", "run", "--host", "0.0.0.0"]
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8080"]