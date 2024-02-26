# Builds the external facing Flask server.
# Should only be built from the compose.yaml file due to relative file paths.

FROM python:3.11-slim-bullseye
LABEL author = "Benjamin Groom"

# Add Flask server files.
WORKDIR /flask
ADD web/*.py .
ADD shared_types.py .
ADD requirements.txt .
RUN pip install -r requirements.txt

# Run the Flask app with Gunicorn.
ENV FLASK_APP=flask_app.py
ENV VOLUME_FILE_PATH=/flask/code_data
ENV PYTHONPYCACHEPREFIX=/flask/code_data
CMD ["python", "flask_app.py"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "flask_app:app", "-w", "4"]