FROM debian:bookworm

# Install updates and dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential curl git python3 python3-poetry pkg-config libssl-dev libgl1 gnupg gpgconf socat \
    libqt5waylandclient5 libqt5waylandcompositor5 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwayland-server0 \
    && rm -rf /var/lib/apt/lists/*

# Install rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy source
COPY ./securedrop-client /src/securedrop-client

# Build proxy
WORKDIR /src/securedrop-client/proxy
RUN pwd && make build

# Install poetry deps
WORKDIR /src/securedrop-client/client
RUN poetry install

# Run
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]