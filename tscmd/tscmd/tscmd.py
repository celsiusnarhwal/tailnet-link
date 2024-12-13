import subprocess
import sys
from pathlib import Path


def main():
    if sys.platform == "win32":
        tailscale = [Path("C:/Program Files/Tailscale/tailscale.exe")]
    else:
        tailscale = ["sudo", "tailscale"]

    subprocess.run(tailscale + sys.argv[1:], shell=True)
