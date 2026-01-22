from pathlib import Path

from src.drivers.metrics_driver import PerformanceMetrics
from src.drivers.path_driver import VideoPathDriver
from src.drivers.websocket_driver import WebsocketVideoManager
from src.streaming.reader import VideoReader

# Caminho absoluto baseado no arquivo atual
VIDEOS_PATH = Path(__file__).parent.parent / "videos"

path = VideoPathDriver(str(VIDEOS_PATH))
metrics = PerformanceMetrics()
reader = VideoReader(path=path, metrics=metrics)


def video_reader() -> VideoReader:
    return reader


def websocket_manager() -> WebsocketVideoManager:
    return WebsocketVideoManager(reader=reader, path=path)
