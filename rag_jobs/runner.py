# Legacy single-tick scheduler (superseded by worker_loop)

from rag_jobs.models import JobStatus

def run_once(store, workers):
    pending = store.list_by_status(JobStatus.PENDING)
    
    for job in pending:
        for worker in workers:
            if worker.can_handle(job):
                worker.execute(job)
                break
