import sys
import traceback
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("FacialAttendance")

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions by logging them."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Let the system handle keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Set the exception hook
sys.excepthook = handle_exception

def log_error(message, exception=None):
    """Log an error message with optional exception details."""
    if exception:
        logger.error(f"{message}: {str(exception)}")
    else:
        logger.error(message)

def log_info(message):
    """Log an information message."""
    logger.info(message)

def log_warning(message):
    """Log a warning message."""
    logger.warning(message)

class FaceRecognitionError(Exception):
    """Exception raised for errors in face recognition."""
    pass

class DatabaseError(Exception):
    """Exception raised for errors in database operations."""
    pass

class StorageError(Exception):
    """Exception raised for errors in storage operations."""
    pass
