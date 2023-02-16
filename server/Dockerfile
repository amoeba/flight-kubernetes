FROM python:3.10

RUN python3 -m pip install pyarrow

WORKDIR /server
ADD server.py .

EXPOSE 8815

ENTRYPOINT [ "python3", "server.py" ]
