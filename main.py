import subprocess
from time import sleep, time
from os import getcwd, path, makedirs
from subprocess import Popen, PIPE
import urllib.request
import json
import sys


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


import os

PORT = int(os.getenv('PORT', 7777))
IP = os.getenv('IP', '127.0.0.1')
SHOULD_UPDATE_GIT = os.getenv('SHOULD_UPDATE_GIT', 'true').lower() == 'true'
TICK_RATE = int(os.getenv('TICK_RATE', 60))
IS_BETA_BRANCH = os.getenv('IS_BETA_BRANCH', 'true').lower() == 'true'
VERSION_ENDPOINT = os.getenv('VERSION_ENDPOINT', 'https://api.nanos.world/game/changelog')
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 900))
#GIT_PACKAGES = json.loads(os.getenv('GIT_PACKAGES', '''[{
#    "name": "NanosWorldServer",
#    "url": "https://github.com/NanosWorld/NanosWorldServer.git", 
#    "branch": "main"
#}]'''))
GIT_PACKAGES = json.loads(os.getenv('GIT_PACKAGES', '[]'))
PROCESS: Popen
FAILED_HEARTBEATS = 0
MAX_FAILED_HEARTBEATS = 10
SERVER_DIR = getcwd() + f"/servers/{PORT}"
LATEST_LOCAL_VERSION = "0"
LATEST_VERSION = "0"

def get_latest_local_version():
    global LATEST_LOCAL_VERSION
    global PROCESS
    should_print = True
    if "PROCESS" in globals():
        should_print = False
    if should_print:
        print(
            f"{bcolors.OKBLUE}[🔍 get local version]{bcolors.ENDC} Checking local version..."
        )
    try:
        version_file = "version.txt"
        if not path.exists(version_file):
            print(
                f"{bcolors.WARNING}[❌ get local version]{bcolors.ENDC} version.txt not found!"
            )
            return False

        f = open(version_file, "r")
        version = f.read().strip()
        if not version:
            print(
                f"{bcolors.WARNING}[⚠️ get local version]{bcolors.ENDC} Empty version file!"
            )
            return False

        LATEST_LOCAL_VERSION = version
        f.close()
        if should_print:
            print(
                f"{bcolors.OKGREEN}[✅ get local version]{bcolors.ENDC} Local version: {LATEST_LOCAL_VERSION}"
            )
        return get_latest_version()
    except Exception as e:
        print(
            f"{bcolors.WARNING}[⚠️ get local version]{bcolors.ENDC} Failed to get local version: {str(e)}"
        )
        print(
            f"{bcolors.OKBLUE}[⬇️ get local version]{bcolors.ENDC} Downloading latest version from Steam..."
        )
        update()
        return False


def set_latest_local_version(version):
    global LATEST_LOCAL_VERSION
    print(
        f"{bcolors.OKBLUE}[💾 set version]{bcolors.ENDC} Saving new version: {version}"
    )
    try:
        version_file = "version.txt"
        f = open(version_file, "w")
        f.write(version)
        f.close()
        LATEST_LOCAL_VERSION = version
        print(
            f"{bcolors.OKGREEN}[✅ set version]{bcolors.ENDC} Version saved successfully!"
        )
    except Exception as e:
        print(
            f"{bcolors.FAIL}[❌ set version]{bcolors.ENDC} Failed to save version: {str(e)}"
        )


def get_latest_version():
    global LATEST_VERSION
    global PROCESS
    should_print = True
    if "PROCESS" in globals():
        should_print = False
    if should_print:
        print(
            f"{bcolors.OKBLUE}[🌐 get latest version]{bcolors.ENDC} Checking latest version from API..."
        )
    try:
        response = urllib.request.urlopen(VERSION_ENDPOINT, timeout=10)
        data = json.load(response)
        if not data:
            print(
                f"{bcolors.FAIL}[❌ get latest version]{bcolors.ENDC} Empty response from API"
            )
            return False

        LATEST_VERSION = data[0]["name"]
        if should_print:
            print(
                f"{bcolors.OKGREEN}[✅ get latest version]{bcolors.ENDC} Latest version: {LATEST_VERSION}"
            )
        if LATEST_VERSION == LATEST_LOCAL_VERSION:
            if should_print:
                print(
                    f"{bcolors.OKGREEN}[✨ get latest version]{bcolors.ENDC} Server is up to date!"
                )
            return True
        else:
            print(
                f"{bcolors.WARNING}[⚠️ get latest version]{bcolors.ENDC} New version available!"
            )
            set_latest_local_version(LATEST_VERSION)
            return False
    except Exception as e:
        print(
            f"{bcolors.FAIL}[❌ get latest version]{bcolors.ENDC} Unexpected error: {str(e)}"
        )
        return False


def tick():
    global PROCESS
    if "PROCESS" not in globals():
        print(f"{bcolors.FAIL}[❌ tick]{bcolors.ENDC} Server process not initialized!")
        return False
    try:
        with urllib.request.urlopen(f"http://{IP}:{PORT}", timeout=5) as response:
            response.read()
        print(f"{bcolors.OKGREEN}[💗 tick]{bcolors.ENDC} Server heartbeat OK")
        return True
    except Exception as e:
        print(f"{bcolors.FAIL}[💔 tick]{bcolors.ENDC} Server is offline!")
        print(f"{bcolors.FAIL}[💔 tick] Error: {str(e)}")
        return False


def kill():
    print(f"{bcolors.OKBLUE}[🔪 kill]{bcolors.ENDC} Terminating server process...")
    global PROCESS
    try:
        PROCESS.kill()
        PROCESS.send_signal(9)
        PROCESS.wait(timeout=10)
        print(
            f"{bcolors.OKGREEN}[✅ kill]{bcolors.ENDC} Server terminated successfully!"
        )
    except Exception as e:
        print(f"{bcolors.FAIL}[❌ kill]{bcolors.ENDC} Error killing server: {str(e)}")


def start():
    print(f"{bcolors.OKBLUE}[🚀 start]{bcolors.ENDC} Launching server...")
    global PROCESS

    server_executable = path.join(SERVER_DIR, "NanosWorldServer.sh")
    if not path.exists(server_executable):
        print(f"{bcolors.FAIL}[❌ start]{bcolors.ENDC} Server executable not found!")
        raise SystemExit

    PROCESS = Popen([""], executable=server_executable, stdin=PIPE, cwd=SERVER_DIR)
    retries = 0
    max_retries = 30

    print(
        f"{bcolors.OKBLUE}[⏳ start]{bcolors.ENDC} Waiting for server to come online..."
    )
    while not tick():
        retries += 1
        print(
            f"{bcolors.WARNING}[🔄 start]{bcolors.ENDC} Attempt {retries}/{max_retries}"
        )
        if retries >= max_retries:
            print(
                f"{bcolors.FAIL}[❌ start]{bcolors.ENDC} Server failed to start after {max_retries} attempts!"
            )
            raise SystemExit
        sleep(1)
    print(f"{bcolors.OKGREEN}[✅ start]{bcolors.ENDC} Server started successfully!")


def restart():
    print(f"{bcolors.OKBLUE}[🔄 restart]{bcolors.ENDC} Initiating server restart...")
    kill()
    sleep(2)  # Give the system some time to clean up
    start()


def update():
    print(f"{bcolors.OKBLUE}[⬆️ update]{bcolors.ENDC} Starting server update...")
    
    # Create server directory if it doesn't exist
    makedirs(SERVER_DIR, exist_ok=True)
    
    steamcmd = [
        "steamcmd",
        "+force_install_dir",
        SERVER_DIR,
        "+login",
        "anonymous",
        "+app_update",
        "1936830",
    ]

    if IS_BETA_BRANCH:
        print(
            f"{bcolors.WARNING}[🧪 update]{bcolors.ENDC} Using beta branch: bleeding-edge"
        )
        steamcmd += ["-beta", "bleeding-edge"]

    steamcmd += ["validate", "+quit"]

    print(f"{bcolors.OKBLUE}[⏳ update]{bcolors.ENDC} Downloading updates...")
    pout = subprocess.run(
        steamcmd, cwd=SERVER_DIR
    )
    if pout.returncode == 0:
        print(
            f"{bcolors.OKGREEN}[✅ update]{bcolors.ENDC} Server updated successfully!"
        )
        get_latest_version()
    else:
        print(
            f"{bcolors.FAIL}[❌ update]{bcolors.ENDC} Update failed (code: {pout.returncode})"
        )
        print(
            f"{bcolors.WARNING}[⚠️ update]{bcolors.ENDC} Please verify steamcmd is installed!"
        )
        raise SystemExit


def send_cmd(cmd):
    global PROCESS
    if cmd is None:
        return False, "Empty command"
    if len(cmd) > 1024:
        return False, "Command too long"
    try:
        cmd += "\n"
        cmd = cmd.encode()
        stdin = PROCESS.stdin
        if stdin is not None:
            stdin.write(cmd)
            stdin.flush()
            print(
                f"{bcolors.OKGREEN}[📝 command]{bcolors.ENDC} Sent: {cmd.decode().strip()}"
            )
            return True, ""
        return False, "No stdin"
    except Exception as e:
        return False, f"Failed to send command: {str(e)}"


def main():
    global FAILED_HEARTBEATS
    global MAX_FAILED_HEARTBEATS
    global PROCESS

    print(f"{bcolors.OKBLUE}[🔄 main]{bcolors.ENDC} Starting main loop...")

    while True:
        tick_status = tick()
        if not tick_status:
            FAILED_HEARTBEATS += 1
            print(
                f"{bcolors.WARNING}[💔 main]{bcolors.ENDC} Failed heartbeats: {FAILED_HEARTBEATS}/{MAX_FAILED_HEARTBEATS}"
            )

        if FAILED_HEARTBEATS >= MAX_FAILED_HEARTBEATS:
            print(
                f"{bcolors.FAIL}[🚨 main]{bcolors.ENDC} Maximum failed heartbeats reached!"
            )
            restart()
            sleep(TICK_RATE * 5)
            FAILED_HEARTBEATS = 0

        # Check for updates every 15 minutes (900 seconds)
        
        if tick_status and (int(time()) % UPDATE_INTERVAL == 0):
            if not get_latest_local_version():
                print(
                    f"{bcolors.WARNING}[⚠️ main]{bcolors.ENDC} Update required - initiating countdown..."
                )

                countdown_messages = [
                    (
                        "chat 🔄 Found a new version of server, updating in 5 minutes, save your stuff!",
                        240,
                    ),
                    ("chat ⚠️ Server is restarting in 1 minute!", 50),
                    ("chat 🕐 Server is restarting in 10 seconds!", 5),
                    ("chat 5️⃣ Server is restarting in 5 seconds!", 1),
                    ("chat 4️⃣ Server is restarting in 4 seconds!", 1),
                    ("chat 3️⃣ Server is restarting in 3 seconds!", 1),
                    ("chat 2️⃣ Server is restarting in 2 seconds!", 1),
                    ("chat 1️⃣ Server is restarting in 1 second!", 1),
                    ("chat 🚀 Server is restarting NOW!", 1),
                ]

                for msg, delay in countdown_messages:
                    send_cmd(msg)
                    sleep(delay)

                update()
                sleep(10)
                restart()

        sleep(TICK_RATE)


def install_git_packages():
    print(f"{bcolors.OKBLUE}[📦 git]{bcolors.ENDC} Installing Git packages...")
    packages_dir = path.join(SERVER_DIR, "Packages")
    makedirs(packages_dir, exist_ok=True)

    for package in GIT_PACKAGES:
        package_name = package["name"]
        package_url = package["url"]
        package_branch = package.get("branch", "main")
        package_dir = path.join(packages_dir, package_name)

        print(f"{bcolors.OKBLUE}[📦 git]{bcolors.ENDC} Installing {package_name}...")

        if path.exists(package_dir):
            print(f"{bcolors.OKBLUE}[📦 git]{bcolors.ENDC} Updating {package_name}...")
            try:
                subprocess.run(["git", "pull"], cwd=package_dir, check=True)
                print(f"{bcolors.OKGREEN}[✅ git]{bcolors.ENDC} {package_name} updated successfully!")
            except subprocess.CalledProcessError as e:
                print(f"{bcolors.FAIL}[❌ git]{bcolors.ENDC} Failed to update {package_name}: {str(e)}")
        else:
            print(f"{bcolors.OKBLUE}[📦 git]{bcolors.ENDC} Cloning {package_name}...")
            try:
                subprocess.run(["git", "clone", "-b", package_branch, package_url, package_dir], check=True)
                print(f"{bcolors.OKGREEN}[✅ git]{bcolors.ENDC} {package_name} installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"{bcolors.FAIL}[❌ git]{bcolors.ENDC} Failed to clone {package_name}: {str(e)}")

    pass

if __name__ == "__main__":
    print(
        f"{bcolors.OKBLUE}[🎮 init]{bcolors.ENDC} Starting Nanos World Server Manager..."
    )
    try:
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((IP, PORT))
        if result == 0:
            print(
                f"{bcolors.FAIL}[🚫 init]{bcolors.ENDC} Port {PORT} is already in use!"
            )
            sys.exit(1)
        sock.close()
    except Exception as e:
        print(
            f"{bcolors.WARNING}[⚠️ init]{bcolors.ENDC} Failed to check port availability: {str(e)}"
        )

    # Create server directory structure
    makedirs(SERVER_DIR, exist_ok=True)

    if not get_latest_local_version():
        print(
            f"{bcolors.WARNING}[⚠️ init]{bcolors.ENDC} No local version found - retrieving latest version..."
        )
        update()
    install_git_packages()
    start()
    main()
