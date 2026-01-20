from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any

from src.interfaces.metrics_interface import IPerformanceMetrics
from src.interfaces.video_path_interface import IVideoPathDriver


@dataclass
class VideoReader:
    path: IVideoPathDriver
    metrics: IPerformanceMetrics

    async def read_chunks(
        self, video_name: str, chunk_size: int = 65536
    ) -> AsyncGenerator[memoryview, Any]:
        if not self.path.video_exists(video_name):
            raise FileNotFoundError(f"Video '{video_name}' not found")

        video_path = self.path.get_video_path(video_name)

        self.metrics.increment_streams()

        with video_path.open("rb") as video_file:
            while True:
                video_chunk = video_file.read(chunk_size)

                if not video_chunk:
                    self.metrics.decrement_streams()
                    break

                self.metrics.record_chunk(len(video_chunk))

                yield memoryview(video_chunk)

    async def read_range(self, video_name: str, start: int, end: int) -> memoryview:
        if not self.path.video_exists(video_name):
            raise FileNotFoundError(f"Video '{video_name}' not found")

        video_path = self.path.get_video_path(video_name)

        with video_path.open("rb") as video_file:
            video_file.seek(start)
            data = video_file.read(end - start)

            return memoryview(data)
