import logging
import sys
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.factories.video_stream_factory import websocket_manager

wbs_router = APIRouter(prefix="/api/ws")
ws_manager = websocket_manager()
# Configurar logging para stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

log = logging.getLogger(__name__)


@wbs_router.websocket("/stream/{video_name}")
async def websocket_streaming(video_name: str, websocket: WebSocket) -> None:
    log.info(video_name)
    client_id = str(uuid.uuid4())

    if not ws_manager.path.video_exists(video_name):
        await websocket.close(code=1003, reason="Video not found")
        return

    await ws_manager.connect(client_id, websocket)

    try:
        await ws_manager.stream_video(client_id, video_name, 0.0)
    except WebSocketDisconnect:
        pass
    except Exception as err:
        log.error("Error in websocket streaming for %s: %s", video_name, str(err), exc_info=True)
    finally:
        await ws_manager.disconnect(client_id)
