import time
from dataclasses import dataclass, field

import psutil

from src.interfaces.metrics_interface import IPerformanceMetrics


@dataclass
class PerformanceMetrics(IPerformanceMetrics):
    _start_time: float = field(default_factory=time.time)
    _bytes_sent: int = field(default=0)
    _chunks_sent: int = field(default=0)
    _active_streams: int = field(default=0)
    current_procces = psutil.Process()

    def record_chunk(self, chunk_size: int) -> None:
        self._bytes_sent += chunk_size
        self._chunks_sent += 1

    def increment_streams(self) -> None:
        self._active_streams += 1

    def decrement_streams(self) -> None:
        self._active_streams -= 1

    def get_metrics(self) -> dict[str, float | int]:
        uptime = time.time() - self._start_time
        mb_sent = self._bytes_sent / 1024 / 1024

        return {
            "uptime_seconds": uptime,
            "bytes_sent": self._bytes_sent,
            "mb_sent": mb_sent,
            "chunks_sent": self._chunks_sent,
            "throughput_mbps": mb_sent / uptime if uptime else 0,
            "active_streams": self._active_streams,
            "memory_mb": self.current_procces.memory_info().rss / 1024 / 1024,
            "cpu_percent": self.current_procces.cpu_percent(),
        }
