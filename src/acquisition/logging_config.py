import logging
from pathlib import Path
def configure_logging():
 Path("logs").mkdir(exist_ok=True)
 logging.basicConfig(filename="logs/hashlink.log",level=logging.INFO)
