from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any


class IVideoReader(ABC):
    @abstractmethod
    async def read_chunks(
        self, video_name: str, chunk_size: int = 65536
    ) -> AsyncGenerator[memoryview, Any]:
        pass

    @abstractmethod
    async def read_range(
        self, video_name: str, start: int, end: int
    ) -> AsyncGenerator[memoryview, Any]:
        pass
