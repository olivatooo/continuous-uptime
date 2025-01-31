#!/usr/bin/env python3

import os
import sys
import subprocess
import platform

# Colors for output
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color


def print_color(color, message):
    print(f"{color}{message}{NC}")


print_color(YELLOW, "Checking your operating system...")

# Detect OS
if sys.platform.startswith("linux"):
    if os.path.isfile("/etc/os-release"):
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("NAME="):
                    OS = line.split("=")[1].strip().strip('"')
                    break
    else:
        OS = "Unknown Linux"
elif sys.platform == "darwin":
    OS = "macOS"
else:
    OS = "Unknown"

print_color(GREEN, f"Detected OS: {OS}")


# Function to check if steamcmd is installed
def check_steamcmd():
    return (
        subprocess.call(
            ["which", "steamcmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        == 0
    )


print_color(YELLOW, "Checking if SteamCMD is installed...")

if check_steamcmd():
    print_color(GREEN, "SteamCMD is already installed!")
else:
    print_color(YELLOW, "SteamCMD not found. Installing...")

    if OS in ["Ubuntu", "Debian GNU/Linux"]:
        print_color(YELLOW, "Installing SteamCMD and dependencies on Debian/Ubuntu...")
        os.system("sudo dpkg --add-architecture i386")
        os.system("sudo apt-get update")
        os.system(
            "sudo apt-get install -y lib32gcc1 steamcmd python3 python3-pip curl wget"
        )
    elif OS in ["CentOS Linux", "Red Hat Enterprise Linux"]:
        print_color(YELLOW, "Installing SteamCMD and dependencies on CentOS/RHEL...")
        os.system("sudo yum install -y epel-release")
        os.system(
            "sudo yum install -y glibc.i686 libstdc++.i686 python3 python3-pip curl wget"
        )
        os.makedirs(os.path.expanduser("~/steamcmd"), exist_ok=True)
        os.chdir(os.path.expanduser("~/steamcmd"))
        os.system(
            "curl -O https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
        )
        os.system("tar -xvzf steamcmd_linux.tar.gz")
    elif OS == "Arch Linux":
        print_color(YELLOW, "Installing SteamCMD and dependencies on Arch Linux...")
        os.system(
            "sudo pacman -Sy --noconfirm lib32-gcc-libs steamcmd python python-pip curl wget"
        )
    elif OS == "macOS":
        print_color(YELLOW, "Installing SteamCMD and dependencies on macOS...")
        if (
            subprocess.call(
                ["which", "brew"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            != 0
        ):
            os.system(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            )
        os.system("brew install python3 wget")
        os.makedirs(os.path.expanduser("~/steamcmd"), exist_ok=True)
        os.chdir(os.path.expanduser("~/steamcmd"))
        os.system(
            "curl -O https://steamcdn-a.akamaihd.net/client/installer/steamcmd_osx.tar.gz"
        )
        os.system("tar -xvzf steamcmd_osx.tar.gz")
    else:
        print_color(RED, f"Unsupported operating system: {OS}")
        sys.exit(1)

    print_color(GREEN, "SteamCMD installation completed!")

# Check and install Python dependencies
print_color(YELLOW, "Checking Python installation and dependencies...")
if (
    subprocess.call(
        ["which", "python3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    != 0
):
    print_color(YELLOW, "Python 3 not found. Installing...")
    if OS in ["Ubuntu", "Debian GNU/Linux"]:
        os.system("sudo apt-get install -y python3 python3-pip")
    elif OS in ["CentOS Linux", "Red Hat Enterprise Linux"]:
        os.system("sudo yum install -y python3 python3-pip")
    elif OS == "Arch Linux":
        os.system("sudo pacman -Sy --noconfirm python python-pip")
    elif OS == "macOS":
        os.system("brew install python3")

print_color(YELLOW, "Starting the main process...")
os.system("python3 main.py")

print_color(GREEN, "Process completed!")
