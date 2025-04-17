import logging
from datetime import datetime

now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
log_file_name = "orderbook_log_(" + now + ").txt"


logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt= "%H:%M:%S",
    handlers=[
        logging.FileHandler("logs/"+ log_file_name),   # write to the file
        logging.StreamHandler()               # Show up in terminal also
    ]
)

logger = logging.getLogger(__name__)
    