from enum import Enum
from datetime import datetime
from uuid import uuid4


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Job:
    def __init__(self, job_type: str, payload: dict):
        self.id = str(uuid4())
        self.last_heartbeat = None # Proof of life timestamp
        self.attempts = 0
        self.job_type = job_type
        self.payload = payload
        self.status = JobStatus.PENDING
        self.error = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<Job {self.id} [{self.job_type}] {self.status}>"

    def is_terminal(self) -> bool:
      return self.status in ("COMPLETED", "FAILED")
