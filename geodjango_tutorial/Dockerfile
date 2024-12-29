FROM continuumio/miniconda3

LABEL maintainer="Bujar Raufi"

# I use the geodjango_tutorial as my project name, adjust to your project name
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=geodjango_tutorial.settings

WORKDIR /app

# Create the environment:
COPY ENV.yml .
RUN conda env create -f ENV.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
ENV PYTHONPATH="/app"

# Exposing the port that the container will operate, feel free to change if port is taken
EXPOSE 8001

# Start the server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
