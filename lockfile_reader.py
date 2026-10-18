
import os
def read_lockfile():
    path = os.path.expandvars(r"%LOCALAPPDATA%\Riot Games\Riot Client\Config\lockfile")
    with open(path) as file:
        content = file.read()
        content_arr = content.split(":")
        
        port = content_arr[2]
        password = content_arr[3]
        
        return port, password


if __name__ == "__main__":
    port, password = read_lockfile()
    print(port, password)