FROM continuumio/miniconda3

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Bundle app source
COPY . /usr/src/app

RUN conda env create -f env.yml

ENV PATH /opt/conda/envs/predadr-flask/bin:$PATH

ENV FLASK_APP app.py

RUN apt-get install -y python python-pip python-virtualenv gunicorn

EXPOSE 5000

CMD ["/usr/bin/gunicorn", "--config", "/usr/src/app/gunicorn_config.py", "app:app"]