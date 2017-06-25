FROM python:3.6

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
RUN pip install -r requirements.txt

ADD . /usr/src/app

# run server
CMD python manage.py runserver -h 0.0.0.0
