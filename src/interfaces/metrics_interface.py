from abc import ABC, abstractmethod


class IPerformanceMetrics(ABC):
    @abstractmethod
    def record_chunk(self, chunk_size: int) -> None:
        pass

    @abstractmethod
    def increment_streams(self) -> None:
        pass

    @abstractmethod
    def decrement_streams(self) -> None:
        pass

    @abstractmethod
    def get_metrics(self) -> dict[str, float | int]:
        pass
