import subprocess
import os
import json
import time


def main():
    # Build containers
    subprocess.run(
        ["podman", "build", "-t", "securedrop/tor", "components/tor/"], check=True
    )
    subprocess.run(
        ["podman", "build", "-t", "securedrop/client", "components/client"],
        check=True,
    )

    # Make sure volume folders exist
    if not os.path.exists("volumes"):
        os.mkdir("volumes")
    if not os.path.exists("volumes/securedrop-tor"):
        os.mkdir("volumes/securedrop-tor")
    if not os.path.exists("volumes/securedrop-client"):
        os.mkdir("volumes/securedrop-client")

    # Load config
    with open("config.json") as f:
        config = json.load(f)

    # Run securedrop-tor
    try:
        subprocess.run(
            ["podman", "kill", "securedrop-tor"], check=True, stdout=subprocess.PIPE
        )
        time.sleep(0.2)
    except subprocess.CalledProcessError:
        pass
    subprocess.run(
        [
            "podman",
            "run",
            "--name=securedrop-tor",
            "--rm",
            # Persistent data
            "-v",
            f"{os.getcwd()}/volumes/securedrop-tor:/var/lib/securedrop-tor",
            # Environment variables
            "-e",
            f"HIDSERV_HOSTNAME={config['hidserv']['hostname']}",
            "-e",
            f"HIDSERV_KEY={config['hidserv']['key']}",
            "-d",
            "securedrop/tor",
        ],
        check=True,
    )

    # Run securedrop-client
    try:
        subprocess.run(
            ["podman", "kill", "securedrop-client"], check=True, stdout=subprocess.PIPE
        )
        time.sleep(0.2)
    except subprocess.CalledProcessError:
        pass
    subprocess.run(
        [
            "podman",
            "run",
            "--name=securedrop-client",
            "--rm",
            "-d",
            # No networking, we'll use tor unix socket instead
            "--network=none",
            # Persistent data
            "-v",
            f"{os.getcwd()}/volumes/securedrop-client:/var/lib/securedrop-client",
            # Mount the tor unix socket
            "-v",
            f"{os.getcwd()}/volumes/securedrop-tor:/var/lib/securedrop-tor",
            # Environment variables
            "-e",
            "SDW_PODMAN=1",
            "-e",
            f"SD_PROXY_ORIGIN=http://{config['hidserv']['hostname']}",
            # Use wayland
            "-v",
            f"{os.environ.get('XDG_RUNTIME_DIR')}/{os.environ.get('WAYLAND_DISPLAY')}:/tmp/{os.environ.get('WAYLAND_DISPLAY')}",
            "-e",
            "XDG_RUNTIME_DIR=/tmp",
            "-e",
            f"WAYLAND_DISPLAY={os.environ.get('WAYLAND_DISPLAY')}",
            "securedrop/client",
        ],
        check=True,
    )


"""
podman run --rm \
-v $(pwd)/volumes/securedrop-client:/sdc-home \
-e SDW_PODMAN=1 \
-v $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/tmp/$WAYLAND_DISPLAY \
-e XDG_RUNTIME_DIR=/tmp \
-e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
securedrop/client
"""
