from re import sub
import requests
import subprocess
from time import sleep
from os import getcwd
from subprocess import Popen, PIPE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PORT = 7777
IP = "127.0.0.1"
TICK_RATE = 60
IS_BETA_BRANCH = True
LATEST_LOCAL_VERSION = "0"
LATEST_VERSION = "0"
VERSION_ENDPOINT = "https://api.nanos.world/game/changelog"
PROCESS : Popen
FAILED_HEARTBEATS = 0
MAX_FAILED_HEARTBEATS = 10


def get_latest_local_version():
    global LATEST_LOCAL_VERSION
    print(bcolors.OKBLUE, "[get local version]", bcolors.ENDC, "checking local version")
    try:
        f = open("version.txt", "r")
        version = f.read().strip()
        LATEST_LOCAL_VERSION = version
        f.close()
        print(bcolors.OKGREEN, "[get local version]", bcolors.ENDC, "local version:", LATEST_LOCAL_VERSION)
        """
            This means the local server is up to date
        """
        return get_latest_version()
    except:
        print(bcolors.WARNING, "[get local version]", bcolors.ENDC, "Failed to get local version, downloading latest version from steam")
        update()
        """
            This means the binary was updated
        """
        return False


def set_latest_local_version(version):
    global LATEST_LOCAL_VERSION
    f = open("version.txt", "w")
    f.write(version)
    f.close()
    LATEST_LOCAL_VERSION = version


def get_latest_version():
    global LATEST_VERSION
    print(bcolors.OKBLUE, "[get latest version]", bcolors.ENDC, "checking latest version from api")
    try:
        LATEST_VERSION = requests.get(VERSION_ENDPOINT).json()[0]["name"]
        print(bcolors.OKGREEN, "[get latest version]", bcolors.ENDC, "latest version:", LATEST_VERSION)
        if LATEST_VERSION == LATEST_LOCAL_VERSION:
            print(bcolors.OKGREEN, "[get latest version]", bcolors.ENDC, "latest version is up to date")
            return True
        else:
            print(bcolors.WARNING, "[get latest version]", bcolors.ENDC, "latest version is not up to date")
            set_latest_local_version(LATEST_VERSION)
            print(bcolors.OKGREEN, "[get latest version]", bcolors.ENDC, "latest version set up")
            return False
    except:
        print(bcolors.FAIL, "[get latest version]", bcolors.ENDC, "failed to get latest version")
        raise SystemExit


def tick():
    global PROCESS
    if 'PROCESS' not in globals():
        print(bcolors.FAIL, "[tick]", bcolors.ENDC, "server is not even defined")
        return False
    try:
        requests.get(f"http://{IP}:{PORT}")
        return True
    except:
        print(bcolors.FAIL, "[tick]", bcolors.ENDC, "server is offline")
        return False


def kill():
    print(bcolors.OKBLUE, "[kill]", bcolors.ENDC, "killing server...")
    global PROCESS
    PROCESS.kill()
    PROCESS.send_signal(9)
    PROCESS.wait()


def start():
    print(bcolors.OKBLUE, "[start]", bcolors.ENDC, "starting server...")
    global PROCESS
    PROCESS = Popen([""], executable="./NanosWorldServer.sh", stdin=PIPE)
    retries = 0
    while not tick():
        retries += 1
        print(bcolors.FAIL, "[start]", bcolors.ENDC, f"server is starting... attempts {retries}")
        sleep(1)


def restart():
    print(bcolors.OKBLUE, "[restart]", bcolors.ENDC, "restarting server...")
    kill()
    start()
    pass


def update():
    """
        Update server using steamcmd
    """
    print(bcolors.OKBLUE, "[update]", bcolors.ENDC, "updating server...")
    cwd = getcwd()
    steamcmd = [
        "steamcmd",
        "+force_install_dir", cwd,
        "+login", "anonymous",
        "+app_update", "1936830",
    ]

    if IS_BETA_BRANCH:
        steamcmd += ["-beta", "bleeding-edge"]

    steamcmd += [
        "validate", "+quit"
    ]
    pout = subprocess.run(steamcmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if pout.returncode == 0:
        print(bcolors.OKGREEN, "[update]", bcolors.ENDC, "server updated!")
        get_latest_version()
    else:
        print(bcolors.FAIL, "[update]", bcolors.ENDC, "failed to update server, error code:", pout.returncode, "make sure you have steamcmd installed")
        raise SystemExit


def send_cmd(cmd):
    global PROCESS
    if cmd is None:
        return False, "Empty command"
    if len(cmd) > 1024:
        return False, "Command too long"
    cmd += "\n"
    cmd = cmd.encode()
    stdin = PROCESS.stdin
    if stdin is not None:
        stdin.write(cmd)
        stdin.flush()
        return True, ""
    return False, "No stdin"


def main():
    """
        This loop checks if the server is online and if not, it restarts it.
    """
    global FAILED_HEARTBEATS
    global MAX_FAILED_HEARTBEATS
    global PROCESS
    while True:
        tick_status = tick()
        if not tick_status:
            FAILED_HEARTBEATS += 1
        if FAILED_HEARTBEATS >= MAX_FAILED_HEARTBEATS:
            print(bcolors.FAIL, "[main]", bcolors.ENDC, "could not reach server...")
            restart()
            sleep(TICK_RATE*5)
            FAILED_HEARTBEATS = 0
        if not get_latest_local_version() and tick_status:
            print(bcolors.OKGREEN, "[main]", bcolors.ENDC, "server is online, but I need to restart it")
            send_cmd("chat found a new version of server, updating in 5 minutes, save your stuff")
            sleep(60*4)
            send_cmd("chat server is restarting in 1 minutes")
            sleep(50)
            send_cmd("chat server is restarting in 10 seconds")
            sleep(10)
            send_cmd("chat server is restarting in 5 seconds")
            sleep(5)
            send_cmd("chat server is restarting in 4 seconds")
            sleep(1)
            send_cmd("chat server is restarting in 3 seconds")
            sleep(1)
            send_cmd("chat server is restarting in 2 seconds")
            sleep(1)
            send_cmd("chat server is restarting in 1 second")
            sleep(1)
            send_cmd("chat server is restarting NOW!")
            sleep(1)
            update()
            restart()
        sleep(TICK_RATE)

if __name__ == "__main__":
    get_latest_local_version()
    start()
    main()
