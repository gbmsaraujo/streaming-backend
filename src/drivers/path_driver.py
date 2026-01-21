from dataclasses import dataclass, field
from pathlib import Path

from src.interfaces.video_path_interface import IVideoPathDriver


@dataclass(frozen=True)
class VideoPathDriver(IVideoPathDriver):
    """Driver para operações de arquivos de vídeo."""

    base_path: str
    _path: Path = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "_path", Path(self.base_path))

        if not self.exists():
            self.ensure_base_exists()

    def exists(self) -> bool:
        """Verifica se o diretório base existe."""
        return self._path.exists()

    def get_video_path(self, video_name: str) -> Path:
        """Retorna o caminho completo do vídeo."""
        return self._path / video_name

    def video_exists(self, video_name: str) -> bool:
        """Verifica se um vídeo específico existe."""
        return self.get_video_path(video_name).is_file()

    def get_video_names(self, pattern: str = "*.mp4") -> list[str]:
        """Retorna apenas os nomes dos vídeos."""
        return [video.name for video in self._path.glob(pattern)]

    def get_video_size(self, video_name: str) -> int:
        """Retorna o tamanho do vídeo em bytes."""
        video_path = self.get_video_path(video_name)
        if not video_path.is_file():
            raise FileNotFoundError(f"Video {video_name} not found")
        return video_path.stat().st_size

    def ensure_base_exists(self) -> None:
        """Garante que o diretório base existe."""
        self._path.mkdir(parents=True, exist_ok=True)

    def delete_video(self, video_name: str, missing_ok: bool = True) -> None:
        """Remove um vídeo específico."""
        self.get_video_path(video_name).unlink(missing_ok=missing_ok)

    def read_video(self, video_name: str, chunk_size: int = -1) -> bytes:
        video_path = self.get_video_path(video_name)
        with Path(video_path).open("rb") as video_file:
            return video_file.read(chunk_size)
