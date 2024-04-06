FROM python:3.12.0-alpine

ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /

# Copy the current directory contents into the container
COPY requirements.lock /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.lock

COPY . .

# CMD to run your programs
CMD ["gunicorn", "-b", "0.0.0.0:80", "src.app:app"]