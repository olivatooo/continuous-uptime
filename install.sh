#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking your operating system...${NC}"

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
elif [ "$(uname)" == "Darwin" ]; then
    OS="macOS"
else
    OS="Unknown"
fi

echo -e "${GREEN}Detected OS: $OS${NC}"

# Function to check if steamcmd is installed
check_steamcmd() {
    if command -v steamcmd &> /dev/null; then
        return 0
    else
        return 1
    fi
}

echo -e "${YELLOW}Checking if SteamCMD is installed...${NC}"

if check_steamcmd; then
    echo -e "${GREEN}SteamCMD is already installed!${NC}"
else
    echo -e "${YELLOW}SteamCMD not found. Installing...${NC}"
    
    case $OS in
        "Ubuntu" | "Debian GNU/Linux")
            echo -e "${YELLOW}Installing SteamCMD and dependencies on Debian/Ubuntu...${NC}"
            sudo dpkg --add-architecture i386
            sudo apt-get update
            sudo apt-get install -y lib32gcc1 steamcmd python3 python3-pip curl wget
            ;;
        "CentOS Linux" | "Red Hat Enterprise Linux")
            echo -e "${YELLOW}Installing SteamCMD and dependencies on CentOS/RHEL...${NC}"
            sudo yum install -y epel-release
            sudo yum install -y glibc.i686 libstdc++.i686 python3 python3-pip curl wget
            mkdir -p ~/steamcmd
            cd ~/steamcmd
            curl -O https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
            tar -xvzf steamcmd_linux.tar.gz
            ;;
        "Arch Linux")
            echo -e "${YELLOW}Installing SteamCMD and dependencies on Arch Linux...${NC}"
            sudo pacman -Sy --noconfirm lib32-gcc-libs steamcmd python python-pip curl wget
            ;;
        "macOS")
            echo -e "${YELLOW}Installing SteamCMD and dependencies on macOS...${NC}"
            # Install Homebrew if not installed
            if ! command -v brew &> /dev/null; then
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python3 wget
            mkdir -p ~/steamcmd
            cd ~/steamcmd
            curl -O https://steamcdn-a.akamaihd.net/client/installer/steamcmd_osx.tar.gz
            tar -xvzf steamcmd_osx.tar.gz
            ;;
        *)
            echo -e "${RED}Unsupported operating system: $OS${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}SteamCMD installation completed!${NC}"
fi

# Check and install Python dependencies
echo -e "${YELLOW}Checking Python installation and dependencies...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 not found. Installing...${NC}"
    case $OS in
        "Ubuntu" | "Debian GNU/Linux")
            sudo apt-get install -y python3 python3-pip
            ;;
        "CentOS Linux" | "Red Hat Enterprise Linux")
            sudo yum install -y python3 python3-pip
            ;;
        "Arch Linux")
            sudo pacman -Sy --noconfirm python python-pip
            ;;
        "macOS")
            brew install python3
            ;;
    esac
fi

echo -e "${YELLOW}Starting the main process...${NC}"
python3 main.py

echo -e "${GREEN}Process completed!${NC}"
