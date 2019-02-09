from ruamel.yaml import YAML
import os
import sys

SAMPLE_TOKEN = '99999999:000AASDFADAAAADFDFAFASD'

BASEDIR = os.path.join(os.environ['HOME'], '.rpi.motion')
DEFAULT_CONFIG_PATH = os.path.join(BASEDIR, 'config.yml')
DEFAULT_IMAGE_DIR = os.path.join(BASEDIR, 'images')

TOKEN = 'token'
IMAGE_DIR = 'image-dir'
SEND_CHATS = 'send-to-chats'

class Config:
    def __init__(self, data):
        self.token = data.get(TOKEN)
        self.image_dir = data.get(IMAGE_DIR) or DEFAULT_IMAGE_DIR
        self.send_to_chats = data.get(SEND_CHATS)

def serialized_sample():
    """Serialize a sample configuration to STDOUT"""
    return YAML().dump({
        TOKEN: SAMPLE_TOKEN,
        IMAGE_DIR: DEFAULT_IMAGE_DIR,
    }, sys.stdout)

def load(config_file=None):
    """Load a rpi.motion configuration from a YAML file (by default, use $HOME/.rpi.motion.yml)"""
    config_path = config_file or DEFAULT_CONFIG_PATH
    data = {}

    with open(config_path) as f:
        data = YAML().load(f)

    return Config(data)

