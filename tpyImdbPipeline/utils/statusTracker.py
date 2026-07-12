import os
from pathlib import Path
from dotenv import load_dotenv
from tpyImdbPipeline.utils.logger import get_logger


# Load environment variables from .env file
load_dotenv()


class StatusTracker:
    """
    Create zero-byte marker files under LOG_PATH/statuses/.
    Methods:
    - create_marker(name): create marker file for `name`
    - has_marker(name): check if marker exists
    - clear_all_markers(): delete all marker files
    """
    def __init__(self, logger=None):
        self.logger = logger or get_logger(__name__)
        log_path = Path(os.getenv("LOG_PATH"))
        self.status_dir = log_path / "statuses"
        self.status_dir.mkdir(parents=True, exist_ok=True)

    def marker_path(self, name: str) -> Path:
        return self.status_dir / f"{name}.marker"

    def create_marker(self, name: str) -> None:
        p = self.marker_path(name)
        try:
            if not p.exists():
                p.touch()
                self.logger.info("Created status marker: %s", p)
        except Exception as e:
            self.logger.error("Failed to create marker %s: %s", p, e)
            raise

    def has_marker(self, name: str) -> bool:
        return self.marker_path(name).exists()

    def clear_all_markers(self) -> None:
        for p in self.status_dir.glob("*.marker"):
            try:
                p.unlink()
                self.logger.info("Deleted status marker: %s", p)
            except Exception as e:
                self.logger.error("Failed to delete marker %s: %s", p, e)
                raise