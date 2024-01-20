# Builds the internal code runner server.
# Should only be built from the compose.yaml file due to relative file paths.

FROM python:3.11-slim-bullseye
LABEL authors="Benjamin Groom"

# Set environment variables.
ENV FLASK_APP=flask_app.py
ENV VOLUME_FILE_PATH=/coderunner/code_data
ENV PYTHONPYCACHEPREFIX=/coderunner/code_data

# Install curl for use in the Scala installation later.
RUN apt update
#RUN apt install net-tools
RUN apt install -y curl

# Download code running packages.
RUN apt -y install gcc
RUN apt -y install g++
RUN apt -y install openjdk-17-jdk

# Install Scala 3.3.1 from source and update path.
RUN curl https://github.com/lampepfl/dotty/releases/download/3.3.1/scala3-3.3.1.tar.gz -L | tar -xz -C /usr/local/bin && \
    mv /usr/local/bin/scala3-3.3.1 /usr/local/bin/scala3 && \
    chmod 555 /usr/local/bin/scala3/bin/scala
ENV PATH="${PATH}:/usr/local/bin/scala3/bin"

# Add the python files to the working directory and install requirements.
WORKDIR /coderunner
ADD runner/*.py .
ADD shared_types.py .
ADD requirements.txt .
RUN pip install -r requirements.txt

# Run Gunicorn server to recieve requests for running code.
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "flask_app:app", "-w", "4"]