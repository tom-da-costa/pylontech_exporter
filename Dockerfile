FROM python:3.10-slim

RUN apt update && \
    apt upgrade -y

RUN useradd -ms /bin/bash user && \
    usermod -a -G dialout user

USER user
WORKDIR /home/user

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY us2000c_prometheus_exporter.py .
# ENTRYPOINT ["python3"]
CMD ["python3", "us2000c_prometheus_exporter.py"]
