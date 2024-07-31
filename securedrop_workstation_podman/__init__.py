import subprocess
import os


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

    # Kill securedrop-tor if it's running
    try:
        subprocess.run(
            ["podman", "kill", "securedrop-tor"], check=True, stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        pass

    # Run securedrop-tor
    subprocess.run(
        [
            "podman",
            "run",
            "--name=securedrop-tor",
            "--network=securedrop",
            "--rm",
            "-d",
            "securedrop/tor",
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