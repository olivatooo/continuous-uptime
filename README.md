# Server Auto-Updater Script

This Python script is designed to automate the update and management process for a game server, specifically for the Nanos World game. The script periodically checks for the latest version of the server binary, compares it with the locally installed version, and updates the server if a newer version is available. Additionally, it monitors the server's status, restarting it if it becomes unresponsive.

## Prerequisites

Before using this script, ensure the following requirements are met:

- Python 3.x
- SteamCMD installed on the system

## Configuration

The script contains several configuration parameters that can be adjusted to suit your setup. These parameters are located at the beginning of the script:

```python
PORT = 7777
IP = "127.0.0.1"
TICK_RATE = 60
IS_BETA_BRANCH = True
LATEST_LOCAL_VERSION = "0"
LATEST_VERSION = "0"
VERSION_ENDPOINT = "https://api.nanos.world/game/changelog"
PROCESS: Popen
FAILED_HEARTBEATS = 0
MAX_FAILED_HEARTBEATS = 10
```

- `PORT`: The port on which the Nanos World server is running.
- `IP`: The IP address of the Nanos World server.
- `TICK_RATE`: The interval (in seconds) between each check for the server's status.
- `IS_BETA_BRANCH`: Set to `True` if using the beta branch of the game server.
- `LATEST_LOCAL_VERSION`: Variable to store the locally installed server version.
- `LATEST_VERSION`: Variable to store the latest available server version from the API.
- `VERSION_ENDPOINT`: The API endpoint to retrieve the latest server version.
- `PROCESS`: Variable to store the server process.
- `FAILED_HEARTBEATS`: Number of consecutive failed heartbeats before considering the server offline.
- `MAX_FAILED_HEARTBEATS`: Maximum allowed consecutive failed heartbeats before triggering a server restart.

## Usage

1. Ensure that SteamCMD is installed on your system.
2. Run the script using the following command:

    ```bash
    python main.py
    ```

3. The script will automatically check for the latest version, update the server if needed, and monitor its status, restarting it if necessary.

**Note:** Make sure to customize the script according to your specific Nanos World server setup and requirements.

## License

This script is provided under the [MIT License](LICENSE). Feel free to modify and distribute it according to your needs.
