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
- 📦 **Git Package Support**: Automatically installs and updates Git packages

## 🛠️ Prerequisites

Before running this script, you'll need:

- Python 3.x installed
- SteamCMD installed and accessible from PATH
- Git installed (for Git package support)
- Basic understanding of server management

## ⚙️ Configuration

The script is configured through environment variables:

- 🔌 `PORT` (default: 7777): Server port number
- 🌐 `IP` (default: 127.0.0.1): Server IP address
- ⏰ `TICK_RATE` (default: 60): Health check interval in seconds
- 🧪 `IS_BETA_BRANCH` (default: true): Enable beta branch updates
- ⏱️ `UPDATE_INTERVAL` (default: 900): Time between update checks in seconds
- 📦 `GIT_PACKAGES` (default: [{"name": "NanosWorldServer", "url": "https://github.com/NanosWorld/NanosWorldServer.git", "branch": "main"}]): JSON array of Git packages to install
- 🎮 `GAMEMODE` (required): Server gamemode to run
- 🔄 `SHOULD_UPDATE_GIT` (default: true): Enable automatic Git package update
