import logging
import logging.handlers
import sys

#get logger
logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.handlers.RotatingFileHandler('logs/wallet-api.log', maxBytes = 10*1024*1024, backupCount = 4)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)