import subprocess
import threading
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

# Project root = parent of the 'app' folder
PROJECT_ROOT = str(Path(__file__).parent.parent)

# Subprocess env with PYTHONPATH so child processes can find the 'app' package
SUBPROCESS_ENV = os.environ.copy()
SUBPROCESS_ENV["PYTHONPATH"] = PROJECT_ROOT


def run_backend():
    try:
        logger.info("starting backend service")
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "8000"],
            check=True,
            env=SUBPROCESS_ENV,
            cwd=PROJECT_ROOT
        )
    except CustomException as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend", e)

def run_frontend():
    try:
        logger.info("Starting Frontend service")
        subprocess.run(
            ["streamlit", "run", "app/frontend/ui.py"],
            check=True,
            env=SUBPROCESS_ENV,
            cwd=PROJECT_ROOT
        )
    except CustomException as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend", e)


if __name__ == "__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()

    except CustomException as e:
        logger.exception(f"CustomException occured: {str(e)}")

