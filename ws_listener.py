import asyncio
import ssl
import websockets
import json
from lockfile_reader import read_lockfile
from api_client import get_headers
from api_client import get_match_state
from game_state import parse_match 
from api_client import get_tokens
from api_client import get_core_game_match
from api_client import get_client_version

async def listen(hud):
    port, password = read_lockfile()
    print(port, password)

    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    headers = get_headers(password)

    async with websockets.connect(f"wss://127.0.0.1:{port}", additional_headers=headers, ssl=ssl_ctx) as ws:
        print("connected")
        await ws.send(json.dumps([5, "OnJsonApiEvent"]))

        async for message in ws:
            try:
                parse = json.loads(message)
                if len(parse) >= 3:
                    data = parse[2]
                    uri = data.get("uri", "")
                    if "core-game" in uri and "matches" in uri:
                        match_id = uri.split('/')[-1]
                        port, password = read_lockfile()
                        access_token, entitlement_token, puuid = get_tokens(port, password)
                        client_version = get_client_version(port, password)
                        raw = get_core_game_match(match_id, "na", "na", access_token, entitlement_token, client_version)
                        game_state = parse_match(raw, puuid)
                        hud.update(f"Map: {game_state.map} | Team: {game_state.my_team}")
                        print("extracted match_id:", match_id)
                        ##print(get_match_state(port, password, match_id))
                        ##print(data)

            except json.JSONDecodeError as e:
                print("JSON error:", e)



if __name__ == "__main__":
    asyncio.run(listen())