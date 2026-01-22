import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import TypedDict

from fastapi import WebSocket, WebSocketDisconnect

from src.interfaces.video_path_interface import IVideoPathDriver
from src.interfaces.video_reader_interface import IVideoReader

log = logging.getLogger(__name__)


class WebSocketType(TypedDict):
    websocket: WebSocket
    video_name: str
    started_at: float | None


@dataclass
class WebsocketVideoManager:
    connections: dict[str, WebSocketType] = field(default_factory=dict, init=False)
    reader: IVideoReader
    path: IVideoPathDriver

    async def connect(self, connection_id: str, ws: WebSocket) -> None:
        await ws.accept()

        self.connections[connection_id] = {
            "websocket": ws,
            "video_name": "",
            "started_at": None,
        }
        log.info(
            "Client connected: %s (active connections: %d)", connection_id, len(self.connections)
        )

    async def disconnect(self, connection_id: str) -> None:
        if connection_id not in self.connections:
            log.debug("Client %s already disconnected", connection_id)
            return

        ws = self.connections[connection_id]["websocket"]

        try:
            await ws.close()
            self.connections.pop(connection_id, None)
            log.info(
                "Client disconnected: %s (active connections: %d)",
                connection_id,
                len(self.connections),
            )
        except Exception as e:
            log.warning("Error closing WebSocket for %s: %s", connection_id, str(e))

    async def stream_video(self, connection_id: str, video_name: str, delay: float = 0.01):
        if not self.connections.get(connection_id, None):
            raise ValueError(f"{connection_id} wasn't found.")

        ws = self.connections[connection_id]["websocket"]

        self.connections[connection_id]["video_name"] = video_name
        self.connections[connection_id]["started_at"] = time.time()

        try:
            async for chunk in self.reader.read_chunks(video_name):
                chunk_bytes = bytes(chunk)
                await ws.send_bytes(chunk_bytes)
                await asyncio.sleep(delay)

        except WebSocketDisconnect:
            log.info("Client %s disconnected during streaming", connection_id)
        except Exception as err:
            log.error("Streaming error for %s: %s", connection_id, str(err), exc_info=True)
            raise
