FROM python:3.6

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
RUN pip install Flask==0.12.1 Flask-Script==2.0.5 Flask-SQLAlchemy==2.2 \
  psycopg2==2.7.1 Flask-Testing==0.6.2 gunicorn==19.7.1

ADD . /usr/src/app

# run server
CMD python manage.py runserver -h 0.0.0.0
