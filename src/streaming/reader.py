import logging
from dataclasses import dataclass

import aiofiles

from src.interfaces.metrics_interface import IPerformanceMetrics
from src.interfaces.video_path_interface import IVideoPathDriver

logger = logging.getLogger(__name__)


@dataclass
class VideoReader:
    path: IVideoPathDriver
    metrics: IPerformanceMetrics

    async def read_chunks(self, video_name: str, chunk_size: int = 65536):
        if not self.path.video_exists(video_name):
            raise FileNotFoundError(f"Video '{video_name}' not found")

        video_path = self.path.get_video_path(video_name)

        self.metrics.increment_streams()

        async with aiofiles.open(video_path, "rb") as video_file:
            while True:
                try:
                    video_chunk = await video_file.read(chunk_size)

                    if not video_chunk:
                        self.metrics.decrement_streams()
                        break

                    self.metrics.record_chunk(len(video_chunk))

                    yield memoryview(video_chunk)
                except OSError as e:
                    logger.error(f"Failed to read chunks in {video_name}: {e}")
                    raise

    async def read_range(self, video_name: str, start: int, end: int, chunk_size: int = 65536):
        if not self.path.video_exists(video_name):
            raise FileNotFoundError(f"Video '{video_name}' not found")

        video_path = self.path.get_video_path(video_name)
        remaining = end - start + 1

        async with aiofiles.open(video_path, "rb") as video_file:
            self.metrics.increment_streams()
            await video_file.seek(start)

            while remaining > 0:
                try:
                    to_read = min(chunk_size, remaining)
                    chunk = await video_file.read(to_read)

                    if not chunk:
                        break

                    remaining -= len(chunk)
                    yield memoryview(chunk)

                except (OSError, ValueError) as e:
                    logger.error(f"Failed to read range in {video_name}: {e}")
                    raise
                finally:
                    self.metrics.decrement_streams()
