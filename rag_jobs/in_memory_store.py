from typing import Dict, List
from .models import Job, JobStatus
from .store import JobStore


class InMemoryJobStore(JobStore):
    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def add(self, job: Job):
        self._jobs[job.id] = job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def list_by_status(self, status: JobStatus) -> List[Job]:
        return [j for j in self._jobs.values() if j.status == status]

    def list_all(self) -> List[Job]:
        return super().list_all() # Implemented method to list all jobs
    
    def claim_next_pending(self):
      for job in self._jobs.values():
          if job.status == JobStatus.PENDING:
              job.status = JobStatus.RUNNING
              return job
      return None
