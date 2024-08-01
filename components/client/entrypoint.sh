#!/bin/bash

socat TCP-LISTEN:9050,fork UNIX-CONNECT:/var/lib/securedrop-tor/socks.sock &

export QT_QPA_PLATFORM=wayland

# TODO: run.sh sets up a bunch of dev stuff, but this should work for prod too
cd /src/securedrop-client/client
poetry run ./run.sh --sdc-home /var/lib/securedrop-client
