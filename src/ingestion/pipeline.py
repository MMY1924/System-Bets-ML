from datetime import datetime
from src.utils.logger import get_logger
from src.db.connection import get_connection

logger = get_logger("INGESTION_PIPELINE")


class IngestionPipeline:

    def __init__(self):
        self.api_requests_used = 0
        self.fixtures_processed = 0

    def run(self):
        logger.info("Starting ingestion pipeline")

        try:
            self._identify_new_fixtures()
            self._log_success()
        except Exception as e:
            self._log_failure(str(e))
            raise

    def _identify_new_fixtures(self):
        """
        Placeholder:
        - Consult API (later)
        - Compare with DB
        - Process only new fixtures
        """
        logger.info("Identifying new fixtures (stub)")
        # TODO: implement API logic

    def _log_success(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO ingestion_log
        VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            self.fixtures_processed,
            self.api_requests_used,
            "SUCCESS",
            None
        ))

        conn.commit()
        conn.close()

    def _log_failure(self, error_message: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO ingestion_log
        VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            self.fixtures_processed,
            self.api_requests_used,
            "FAILED",
            error_message
        ))

        conn.commit()
        conn.close()
