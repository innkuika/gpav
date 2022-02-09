# ref https://ep2020.europython.eu/media/conference/slides/CeKGczx-best-practices-for-production-ready-docker-packaging.pdf
# ref https://pythonspeed.com/articles/multi-stage-docker-python/

# builder outputs a virtualenv with installed dependencies
FROM python:3.9-slim-buster AS builder

# makes sure system is up-to-date
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# use regular user
RUN useradd --create-home app
USER app
WORKDIR /home/app

# creates a venv and install dependencies
RUN python -m venv venv
ENV PATH="./venv/bin:$PATH"
COPY requirements.txt .
COPY requirements.prod.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements.prod.txt

# runner intakes the builder's virtualenv, does various things and define an entrypoint
FROM python:3.9-slim-buster AS runner

# use regular user
RUN useradd --create-home app
USER app
WORKDIR /home/app

# intakes the virtualenv from builder
COPY --from=builder /home/app/venv ./venv

# copy in only neccessary files
COPY gpav/ /home/app/gpav
COPY gpav_app/ /home/app/gpav_app
COPY static/ /home/app/static
COPY manage.py .

# pre-compile bytecode and enable PYTHONFAULTHANDLER (catches error in c)
ENV PATH="./venv/bin:$PATH"
ENV PYTHONFAULTHANDLER=1
ENV PORT=5000
EXPOSE 5000
ENTRYPOINT ["gunicorn", "gpav.wsgi", "--log-file", "-"]
