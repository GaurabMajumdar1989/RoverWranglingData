from threading import Thread
import time
from rag_jobs.in_memory_store import InMemoryJobStore
from rag_jobs.models import Job
from rag_jobs.ingestion_worker import IngestionWorker
from rag_jobs.threaded_runner import worker_loop
from rag_jobs.reconciler_runner import reconciler_loop
from rag_core.config import PROJECT_ROOT


doc_path = (PROJECT_ROOT / "fantasy_doc.txt").resolve()

payload={
    "path": str(doc_path)
}

def main():
    # Job store
    store = InMemoryJobStore()

    # Workers
    workers = [IngestionWorker()]

    # Create a job
    job = Job(
        job_type="INGEST_DOCUMENT",
        payload=payload
    )
    store.add(job)

    print("Job created:", job)

    # Start background worker thread
    worker_thread = Thread(
        target=worker_loop,
        args=(store, workers),
        daemon=True
    )
    worker_thread.start()

    #Start background Reconciler Thread
    reconciler_thread = Thread(
        target=reconciler_loop,
        args=(store,5),
        daemon=True
    )
    reconciler_thread.start()

    # Poll job status (simulating API polling)
    while True:
        current_job = store.get(job.id)
        print("Job status:", current_job.status)

        if current_job.status in ("COMPLETED", "FAILED"):
            print("Final job state:", current_job)
            break

        time.sleep(1)


if __name__ == "__main__":
    main()
