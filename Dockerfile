FROM ubuntu:14.04
MAINTAINER Nhat Vo Van <v2nhat@gmail.com>

RUN apt-get update && apt-get install -y \
        git \
        libpq-dev \
        python-dev \
        python-pip

ENV project project

WORKDIR /ank/${project}
COPY . /ank/${project}

RUN pip install -r ank

ENV PYTHONPATH $PYTHONPATH:/ank/${project}
RUN pip install -r /ank/${project}/requirements.txt

ENV PORT 15372
EXPOSE 15372

CMD ["start_app"]