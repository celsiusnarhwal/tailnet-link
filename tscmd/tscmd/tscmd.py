import os
import subprocess
import sys
from pathlib import Path


def main():
    if sys.platform == "win32":
        tailscale = [Path("C:/Program Files/Tailscale/tailscale.exe")]
    else:
        tailscale = ["sudo", Path(os.getenv("_TAILNET_LINK_TAILSCALE_BIN_PATH"))]

    subprocess.run(tailscale + sys.argv[1:])
