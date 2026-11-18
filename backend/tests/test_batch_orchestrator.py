import pytest
from app.pipeline.batch_orchestrator import BatchPipelineOrchestrator, BatchStatus

def test_batch_submission_and_execution():
    orchestrator = BatchPipelineOrchestrator()
    job = orchestrator.submit_batch(["asset-01", "asset-02"])
    assert job.status == BatchStatus.PENDING
    completed = orchestrator.execute_job_synchronous(job.job_id)
    assert completed.status == BatchStatus.COMPLETED
    assert completed.progress == 1.0
