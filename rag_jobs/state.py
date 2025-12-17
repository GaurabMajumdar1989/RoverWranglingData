from datetime import datetime
from .models import JobStatus


def mark_running(job):
    job.status = JobStatus.RUNNING
    job.updated_at = datetime.utcnow()


def mark_completed(job):
    job.status = JobStatus.COMPLETED
    job.updated_at = datetime.utcnow()


def mark_failed(job, error: str):
    job.status = JobStatus.FAILED
    job.error = error
    job.updated_at = datetime.utcnow()

def heartbeat(job):
    job.last_heartbeat = datetime.utcnow()
    