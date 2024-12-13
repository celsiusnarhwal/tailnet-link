import os
import subprocess
import sys
from pathlib import Path


def main():
    if not (sys.argv[1] == "logout" and os.getenv("_TAILNET_LINK_DO_NOT_DISCONNECT")):
        if sys.platform == "win32":
            tailscale = [Path("C:/Program Files/Tailscale/tailscale.exe")]
        else:
            tailscale = ["sudo", "tailscale"]

        subprocess.run(tailscale + sys.argv[1:])
