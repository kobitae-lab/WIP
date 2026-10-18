import threading
import asyncio
from hud import HUD
from ws_listener import listen

def run_listener(hud):
    asyncio.run(listen(hud))

if __name__ == "__main__":
    hud = HUD()
    t = threading.Thread(target=run_listener, args=(hud,), daemon=True)
    t.start()
    hud.run()
