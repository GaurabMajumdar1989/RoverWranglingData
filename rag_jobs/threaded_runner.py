import threading
import time

def worker_loop(store, workers, poll_interval=1):
    while True:
        job = store.claim_next_pending()
        if not job:
            time.sleep(poll_interval)
            continue

        for worker in workers:
            if worker.can_handle(job):
                worker.execute(job)
                break
