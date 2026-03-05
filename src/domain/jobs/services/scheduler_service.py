from datetime import datetime

class SchedulerService:
    def schedule(self, job_id: int, run_at: datetime) -> dict[str, object]:
        return {
            "job_id": job_id,
            "run_at": run_at,
            "status": "scheduled",
        }
