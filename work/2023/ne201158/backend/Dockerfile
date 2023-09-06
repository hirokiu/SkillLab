FROM --platform="linux/amd64" golang:1.20-bookworm AS local

# install tools from apt
RUN apt-get update && \
  apt-get install -y --no-install-recommends ca-certificates tzdata && \
  rm -rf /var/cache/apt/*

WORKDIR /tmp

# Install hot reload
RUN go install github.com/cosmtrek/air@latest

# Download zundamon core
RUN curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/download-linux-x64 -o download && \
  chmod +x download

# Install zundamon core
RUN ./download && \
    rm ./download

# Create symbolic link
RUN ln -s /tmp/voicevox_core/libvoicevox_core.so /usr/local/lib && \
  ln -s /tmp/voicevox_core/voicevox_core.h /usr/local/include && \
  ln -s /tmp/voicevox_core/libonnxruntime.so.1.13.1 /usr/local/lib && \
  ln -s /tmp/voicevox_core/model /usr/local/lib/model

# Reload library cache
RUN ldconfig

WORKDIR /backend/cmd

CMD ["air"]
