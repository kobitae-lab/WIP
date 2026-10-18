import base64
from lockfile_reader import read_lockfile
from game_state import parse_match
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_headers(password):
    credential = "riot:" + password

    auth = {
        "Authorization" : "Basic " + base64.b64encode(credential.encode()).decode()
    }

    return auth

def get_session():
    port, password = read_lockfile()

    headers = get_headers(password)

    response = requests.get(f"https://127.0.0.1:{port}/product-session/v1/external-sessions", headers=headers, verify=False)
    return response.json()


def get_match_state(port, password, match_id):
    headers = get_headers(password)
    response = requests.get(f"https://127.0.0.1:{port}/core-game/v1/matches/{match_id}", headers=headers, verify=False)
    return response.json()


def get_tokens(port, password):
    headers = get_headers(password)
    response = requests.get(f"https://127.0.0.1:{port}/entitlements/v1/token", headers=headers, verify=False)
    data = response.json()
    return data.get("accessToken"), data.get("token"), data.get("subject")

def get_remote_headers(access_token, entitlement_token, client_version):
    riot_api_headers = {
        "Authorization" : "Bearer " + access_token,
        "X-Riot-Entitlements-JWT" : entitlement_token,
        "X-Riot-ClientPlatform" : "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
        "X-Riot-ClientVersion" : client_version
    }

    return riot_api_headers

def get_client_version(port, password):
    data = get_session()
    for key, value in data.items():
        if isinstance(value, dict) and value.get("version"):
            return value.get("version")

def get_core_game_match(match_id, region, shard, access_token, entitlement_token, client_version):
    headers = get_remote_headers(access_token, entitlement_token, client_version)
    response = requests.get(f"https://glz-{region}-1.{shard}.a.pvp.net/core-game/v1/matches/{match_id}", headers=headers)
    return response.json()
    
def get_match_loadouts(match_id, region, shard, access_token, entitlement_token, client_version):
    headers = get_remote_headers(access_token, entitlement_token, client_version)
    response = requests.get(f"https://glz-{region}-1.{shard}.a.pvp.net/core-game/v1/matches/{match_id}/loadouts", headers=headers)
    return response.json()

if __name__ == "__main__":
    port, password = read_lockfile()
    result = get_session()
    client_version = get_client_version(port, password)
    accessToken, entitlement_token, puuid = get_tokens(port, password)
    raw_data = get_core_game_match("ef157125-0ef2-46d6-bf6e-97c0c9b30b1d", "na", "na", accessToken, entitlement_token, client_version)
    loadouts = get_match_loadouts("aaa7dff0-861e-4e49-a1db-a6da3ce1536a", "na", "na", accessToken, entitlement_token, client_version)
    print(loadouts)
    #print(parse_match(raw_data, puuid))
