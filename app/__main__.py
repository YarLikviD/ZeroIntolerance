from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from random import randint

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class Player:
    def __init__(self, websocket) -> None:
        self.pos = {"x":100, "y":145}
        self.web_socket = websocket

class ConnectionManager:
    def __init__(self):
        self.players: list[Player] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        Player(websocket)
        self.players.append(Player(websocket))

    def disconnect(self, websocket: WebSocket):
        for p in self.players:
            if websocket == p.web_socket:
                self.players.remove(p)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self):
        positions = []
        [positions.append(player.pos) for player in self.players]
        [await player.web_socket.send_json(positions) for player in self.players]   
        


manager = ConnectionManager()


@app.get("/")
async def root():
    return FileResponse('app/static/index.html')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.broadcast()
    try:
        while True:
            data = await websocket.receive_json()
            for p in manager.players:
                if websocket == p.web_socket:
                    p.pos = data
                    print(p.pos)
            print(manager.players)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
