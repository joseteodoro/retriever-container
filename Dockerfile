# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the server script and create the uploads directory
COPY webserver.py /app/
RUN mkdir /app/uploads

# Expose the port that the server will listen on (change if necessary)
EXPOSE 8000

# Run the server when the container launches
CMD ["python", "webserver.py"]