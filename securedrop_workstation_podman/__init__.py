import subprocess
import os
import json
import time


def main():
    # Build containers
    subprocess.run(["podman", "build", "-t", "securedrop/tor", "tor/"], check=True)
    subprocess.run(["podman", "build", "-t", "securedrop/client", "-f", "./Dockerfile-client"], check=True)

    # Make sure volume folders exist
    if not os.path.exists("volumes"):
        os.mkdir("volumes")
    if not os.path.exists("volumes/securedrop-client"):
        os.mkdir("volumes/securedrop-client")

    # Create the securedrop podman network
    try:
        subprocess.run(["podman", "network", "create", "securedrop"], check=True)
    except subprocess.CalledProcessError:
        pass

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
            "--network=securedrop",
            "--rm",
            "-e", f"HIDSERV_HOSTNAME={config['hidserv']['hostname']}",
            "-e", f"HIDSERV_KEY={config['hidserv']['key']}",
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
            "--network=securedrop",
            "--rm",
            "-d",
            # Persistent data
            "-v", f"{os.getcwd()}/volumes/securedrop-client:/sdc-home",
            # Environment variables for securedrop-client
            "-e", f"SD_PROXY_ORIGIN=http://{config['hidserv']['hostname']}",
            # Tell the client it's running in podman
            "-e", "SDW_PODMAN=1",
            # Use wayland
            "-v", f"{os.environ.get('XDG_RUNTIME_DIR')}/{os.environ.get('WAYLAND_DISPLAY')}:/tmp/{os.environ.get('WAYLAND_DISPLAY')}",
            "-e", "XDG_RUNTIME_DIR=/tmp",
            "-e", f"WAYLAND_DISPLAY={os.environ.get('WAYLAND_DISPLAY')}",
            "securedrop/client"
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