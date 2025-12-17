import time
from rag_jobs.reconciler import reconcile

def reconciler_loop(store, interval=5):
    while True:
        reconcile(store)
        time.sleep(interval)
