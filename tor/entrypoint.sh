#!/bin/bash

# Configure torrc
cat <<EOF > /etc/tor/torrc
DataDirectory /var/lib/tor
SocksPort 9050
Log notice file /var/log/tor/log
EOF

# Configure authdir
mkdir -p /var/lib/tor/authdir
chown debian-tor:debian-tor /var/lib/tor/authdir
chmod 700 /var/lib/tor/authdir
echo "$HIDSERV_HOSTNAME:descriptor:x25519:$HIDSERV_KEY" > /var/lib/tor/authdir/app-journalist.auth_private
chown debian-tor:debian-tor /var/lib/tor/authdir/app-journalist.auth_private
chmod 600 /var/lib/tor/authdir/app-journalist.auth_private

# Start tor
exec sudo -u debian-tor tor -f /etc/tor/torrc
