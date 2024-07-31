import subprocess


def main():
    # Build the containers
    print("Building securedrop/tor")
    subprocess.run(["podman", "build", "-t", "securedrop/tor", "tor/"], check=True)

    # Create the securedrop podman network, if it doesn't exist
    try:
        subprocess.run(["podman", "network", "create", "securedrop"], check=True)
    except subprocess.CalledProcessError:
        pass
    print("Network 'securedrop' created")

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
