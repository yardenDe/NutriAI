import logging
import sys

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    file_handler = logging.FileHandler("server.log", mode='w', encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[file_handler, stream_handler]
    )
    
    logger = logging.getLogger("NutriAI")
    logger.info("Logging system initialized successfully. Mode: Overwrite")
    
    return logger