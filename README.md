# 🎮 Nanos World Server Manager

A powerful Python script that automates and manages your Nanos World game server with features like automatic updates, health monitoring, graceful restarts, and player notifications.

## ✨ Key Features

- 🔄 **Automatic Updates**: Monitors and installs new server versions automatically
- 💗 **Health Monitoring**: Continuously checks server health with configurable heartbeat system
- 🚀 **Smart Restarts**: Gracefully restarts the server with player notifications
- 📢 **Player Communication**: Sends countdown messages before updates/restarts
- 🧪 **Beta Branch Support**: Optional bleeding-edge version testing
- 🛡️ **Crash Recovery**: Automatically recovers from crashes and hangs
- 🔍 **Version Tracking**: Maintains version history in local files
- ⚡ **Fast Response**: Quick detection and handling of server issues

## 🛠️ Prerequisites

Before running this script, you'll need:

- Python 3.x installed
- SteamCMD installed and accessible from PATH
- Basic understanding of server management

## ⚙️ Configuration

The script is highly configurable through these parameters:

- 🔌 `PORT` (default: 7777): Which door number the server uses to talk to players
- 🌐 `IP` (default: 127.0.0.1): The server's home address on the internet
- ⏰ `TICK_RATE` (default: 60): How often (in seconds) we check if the server is still alive and kicking
- 🧪 `IS_BETA_BRANCH` (default: True): Want to try new experimental features? Set this to True!
- 📱 `LATEST_LOCAL_VERSION` (default: "0"): Keeps track of what version you're running
- 🎮 `LATEST_VERSION` (default: "0"): The newest version available to download
- 🔗 `VERSION_ENDPOINT`: Where we check for new versions of the game
- 🤖 `PROCESS`: The actual server program running on your computer
- 💔 `FAILED_HEARTBEATS` (default: 0): How many times in a row the server didn't respond
- ❤️ `MAX_FAILED_HEARTBEATS` (default: 10): How many missed heartbeats before we restart the server

## 📚 Installation

To get started, simply run the install script:

```bash
git clone https://github.com/olivatooo/continuous-uptime && cd continuous-uptime && bash install.sh
```

## 📖 Usage

To start the server, run:

```bash
python3 main.py
```
