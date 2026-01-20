from abc import ABC, abstractmethod
from pathlib import Path


class IVideoPathDriver(ABC):
    @abstractmethod
    def exists(self) -> bool:
        pass

    @abstractmethod
    def get_video_path(self, video_name: str) -> Path:
        pass

    @abstractmethod
    def video_exists(self, video_name: str) -> bool:
        pass


    @abstractmethod
    def get_video_names(self, pattern: str = "*.mp4") -> list[str]:
        pass

    @abstractmethod
    def get_video_size(self, video_name: str) -> int:
        pass

    @abstractmethod
    def ensure_base_exists(self) -> None:
        pass

    @abstractmethod
    def delete_video(self, video_name: str, missing_ok: bool = True) -> None:
        pass

    @abstractmethod
    def read_video(self, video_name: str, chunk_size:int=-1) -> bytes:
        pass
