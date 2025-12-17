from typing import Dict, List
from .models import Job, JobStatus


class JobStore:
    def add(self, job: Job):
        raise NotImplementedError

    def get(self, job_id: str) -> Job | None:
        raise NotImplementedError

    def list_by_status(self, status: JobStatus) -> List[Job]:
        raise NotImplementedError

    def list_all(self) -> list[Job]:
        raise NotImplementedError   

    def claim_next_pending(self) -> Job | None:
      raise NotImplementedError     