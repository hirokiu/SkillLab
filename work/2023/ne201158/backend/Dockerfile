FROM --platform=amd64/linux golang:1.19.12-bookworm AS local

# install tools from apt
RUN apt-get update && \
  apt-get install -y --no-install-recommends ca-certificates tzdata && \
  rm -rf /var/cache/apt/*

# Install hot reload
RUN go install github.com/cosmtrek/air@latest

# Download zundamon core
RUN binary=download-linux-x64 && \
  curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/${binary} -o download && \
  chmod +x download && \
  ./download

WORKDIR /backend/cmd

CMD ["air"]
