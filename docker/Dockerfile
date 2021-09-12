FROM python3.9

RUN mkdir /workspace
WORKDIR /workspace
ADD requirements.txt .
ADD dev-requirements.txt .
ADD Makefile .
RUN PYTHON=$(which python3) make dev-install

ADD coturn .
ADD tests .

ENTRYPOINT [ "python3" ]