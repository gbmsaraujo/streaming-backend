from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator


class IVideoReader(ABC):
    @abstractmethod
    async def read_chunks(
        self, video_name: str, chunk_size: int = 65536
    ) -> AsyncGenerator[memoryview, Any]:
        pass

    @abstractmethod
    async def read_range(self, video_name: str, start: int, end: int) -> memoryview:
        pass
