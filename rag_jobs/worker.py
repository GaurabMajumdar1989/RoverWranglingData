from abc import ABC, abstractmethod
from .models import Job

class Worker(ABC):
    @abstractmethod
    def can_handle(self, job: Job) -> bool:
        pass

    @abstractmethod
    def execute(self, job: Job):
        pass
  