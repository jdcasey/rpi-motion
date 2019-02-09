import requests
from os.path import (join, isdir)
from os import makedirs
import shutil
import datetime as dt
import logging

MOTION_SNAPSHOT_URL='http://localhost:8080/0/action/snapshot'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def take_snapshot(cfg):
    r = requests.get(MOTION_SNAPSHOT_URL, stream=True)
    if r.status_code == 200:
        logger.info("Saving snapshot.")
        return True
    else:
        logger.warning(f"Cannot save snapshot. Response was: {r.status_code}")

    return False
