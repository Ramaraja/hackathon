# Using ubuntu image like a base

FROM ubuntu:16.04

# Installing python and requirements
RUN    apt-get update && apt-get -y install curl python python-pip vim \
python-tk && apt-get clean
RUN    pip install --upgrade pip
RUN    mkdir -p ~/.pip/
COPY . /hackathon
RUN    pip install --no-cache-dir -r /hackathon/requirements.txt
RUN    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN    pip install requests
RUN    mkdir -p /hackathon

# Set the working directory
WORKDIR /hackathon

RUN chmod +x /hackathon/run.sh
RUN chmod +x /hackathon/app.py

ENTRYPOINT ["/bin/bash","/hackathon/run.sh"]
