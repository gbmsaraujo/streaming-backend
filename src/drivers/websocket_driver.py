import asyncio
import time
from dataclasses import field
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
from src.interfaces.video_reader import IVideoReader


class WebsocketVideoManager:
    connections: dict[str, dict[str, Any]] = field(default={})
    ws: WebSocket
    reader: IVideoReader

    async def connect(self, connection_id: str) -> None:
        await self.ws.accept()

        self.connections[connection_id] = {
            "websocket": self.ws,
            "video_name": "",
            "started_at": None,
        }
        print(f"id {connection_id} is completed [check how get active connections]")

    def disconnect(self, connection_id: str) -> None:
        if connection_id not in self.connections:
            raise ValueError(f"{connection_id}  wasn't found.")

        self.connections.pop(connection_id)

        print(f"id {connection_id} was removed [check how get active connections]")

    async def stream_video(self, connection_id: str, video_name):
        if not self.connections.get(connection_id, None):
            raise ValueError(f"{connection_id} wasn't found.")

        ws = self.connections["websocket"]

        self.connections[connection_id]["video_name"] = video_name
        self.connections[connection_id]["started_at"] = time.time()

        while True:
            try:
                async for chunk in self.reader.read_chunks(video_name):
                    chunk_bytes = bytes(chunk)
                    await self.ws.send_bytes(chunk_bytes)
                    await asyncio.sleep(0.01)

            except WebSocketDisconnect:
                self.disconnect(connection_id)
                print("Client was disconnected")
