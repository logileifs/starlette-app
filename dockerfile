FROM python:3.7
MAINTAINER logileifs <logileifs@gmail.com>

RUN apt-get update
RUN apt-get install -y redis-tools
RUN pip install --upgrade pip

ADD api/ /api
ADD run.sh run.sh
ADD start.sh start.sh
ADD prestart.sh prestart.sh
ADD requirements requirements

RUN pip install -r requirements

#RUN pip3 install pipenv
#RUN pipenv install --system

#ENTRYPOINT ["/bin/ping"]
CMD ["/bin/bash", "run.sh"]
