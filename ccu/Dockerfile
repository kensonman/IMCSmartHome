# Name: bt.advform
# Author: Kenson Man <kenson@breakthrough.org.hk>
# Desc:   The file used to create the docker container that provide the advform application.
FROM django:1.9-python3
MAINTAINER Kenson Man <kenson@kenson.idv.hk>
ARG UID=1000
ARG GID=1000
ARG USERNAME=docker

ADD requirements.txt /usr/src/app/

RUN echo "Installating the system dependencies..." 	&& \
  echo "alias ll=\"ls -l\"" >> /root/.bashrc 		&& \
  apt-get update && apt-get install --fix-missing -y libpq-dev python3-dev libsasl2-dev libldap2-dev libssl-dev vim libjpeg-dev python-dateutil && \
  pip install --upgrade pip 				&& \
  echo "Installating the django dependencies..."	&& \
  pip install -r /usr/src/app/requirements.txt		&& \
  echo "Creating the user<${USERNAME}::${UID}> and group<${GID}>..."			&& \
  groupadd -g ${GID} ${USERNAME}			&& \
  useradd -u ${UID} -g ${GID} -M -d /usr/src/app ${USERNAME}	&& \
  echo "Generating the startup scripts..."		&& \
  echo "#/bin/bash" > /startup				&& \
  echo "python /usr/src/app/manage.py runserver 0.0.0.0:8000" >> /startup && \
  echo "alias ll='ls -l'" >> ~/.bashrc			&& \
  chown ${UID}:${GID} /startup				&& \
  chmod 700 /startup

WORKDIR /usr/src/app
USER ${USERNAME}
EXPOSE 8000
CMD /startup
