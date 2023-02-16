FROM python:3.10

RUN python3 -m pip install pyarrow

WORKDIR /client
ADD client.py .

ENTRYPOINT [ "python3", "client.py" ]
