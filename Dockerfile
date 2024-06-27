FROM python:3.9-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pygame \
    libsdl1.2debian \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libx11-6 \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV XDG_RUNTIME_DIR=/tmp/runtime-user
ENV SDL_AUDIODRIVER=dummy

RUN mkdir -p $XDG_RUNTIME_DIR && chmod 0700 $XDG_RUNTIME_DIR


COPY . /app


RUN pip install --no-cache-dir pygame pymongo flask

CMD ["python", "app.py"]
