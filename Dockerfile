FROM python:3.12.0-slim-buster

# Set the working directory
WORKDIR /src

# Copy the current directory contents into the container at /src
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# CMD to run your programs
CMD ["gunicorn", "-b", "0.0.0.0:80", "src.app:app"]