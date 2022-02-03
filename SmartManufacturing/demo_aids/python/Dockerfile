FROM python:3.8-slim

WORKDIR /app
COPY queryGateway_ProTegoHack.py queryGateway_ProTegoHack.py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
ENTRYPOINT ["python3"]
EXPOSE 9005
ENV PYTHONUNBUFFERED=1
CMD ["queryGateway_ProTegoHack.py"]
