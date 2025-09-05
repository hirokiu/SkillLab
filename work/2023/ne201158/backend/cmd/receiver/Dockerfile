FROM golang:1.20-bookworm AS local

# install tools from apt
RUN apt-get update && \
  apt-get install -y --no-install-recommends ca-certificates tzdata && \
  rm -rf /var/cache/apt/*

WORKDIR /tmp

# Install hot reload
RUN go install github.com/cosmtrek/air@latest

WORKDIR /backend/cmd/receiver

CMD ["air"]
