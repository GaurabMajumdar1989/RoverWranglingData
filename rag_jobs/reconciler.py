from datetime import datetime, timedelta
from rag_jobs.models import JobStatus

STALE_AFTER = timedelta(seconds=10)
MAX_ATTEMPTS = 3

def find_stale_jobs(store):
    now = datetime.utcnow()
    stale = []

    for job in store.list_by_status(JobStatus.RUNNING):
        if job.last_heartbeat is None:
            stale.append(job)
        elif now - job.last_heartbeat > STALE_AFTER:
            stale.append(job)

    return stale

def reconcile(store):
    stale_jobs = find_stale_jobs(store)

    for job in stale_jobs:
        if job.attempts >= MAX_ATTEMPTS:
            job.status = JobStatus.FAILED
            job.error = "Max retries exceeded"
        else:
            job.status = JobStatus.PENDING