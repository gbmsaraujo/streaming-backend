from src.drivers.metrics_driver import PerformanceMetrics
from src.drivers.path_driver import VideoPathDriver
from src.streaming.reader import VideoReader

path = VideoPathDriver("./src/videos/")
metrics = PerformanceMetrics()


def video_reader() -> VideoReader:
    return VideoReader(path=path, metrics=metrics)
