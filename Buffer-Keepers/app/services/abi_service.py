import json
import logging
import os
import time
from json.decoder import JSONDecodeError
from typing import Optional

import requests
from cache import cache

logger = logging.getLogger(__name__)


def get_abi(
    abi_path: str,
):
    with open(abi_path) as f:
        abi = json.load(f)
    return abi
