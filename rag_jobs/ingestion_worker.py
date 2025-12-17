from rag_jobs.worker import Worker
from rag_jobs.state import mark_running, mark_completed, mark_failed, heartbeat
from rag_jobs.models import Job


# Phase 2 imports (read-only usage)
from rag_core.ingest import ingest_with_faiss
from rag_core.ingest import load_document, chunk_text


class IngestionWorker(Worker):
    def can_handle(self, job: Job) -> bool:
        return job.job_type == "INGEST_DOCUMENT"

    def execute(self, job: Job):
        try:
            print(f"job inside execute from ingest_worker: {job}")
            print(f"job path from ingest_worker: {job.payload['path']}")
            mark_running(job)
            job.attempts += 1
            heartbeat(job)
            path = job.payload["path"]
            text = load_document(path)
            chunks = chunk_text(text)

            ingest_with_faiss(path, chunks)

            mark_completed(job)

        except Exception as e:
            mark_failed(job, str(e))
