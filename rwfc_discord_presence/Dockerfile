ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG C.UTF-8

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY run.py /run.py

CMD ["python3", "/run.py"]