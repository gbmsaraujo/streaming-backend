from src.drivers.metrics_driver import PerformanceMetrics
from src.drivers.path_driver import VideoPathDriver
from src.drivers.websocket_driver import WebsocketVideoManager
from src.streaming.reader import VideoReader

path = VideoPathDriver("./src/videos/")
metrics = PerformanceMetrics()
reader = VideoReader(path=path, metrics=metrics)


def video_reader() -> VideoReader:
    return reader


def websocket_manager() -> WebsocketVideoManager:
    return WebsocketVideoManager(reader=reader, path=path)
