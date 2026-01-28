import argparse
import logging
import os
import sys
from typing import Any, Dict, List

import thonny
from thonny import (
    SINGLE_INSTANCE_DEFAULT,
    choose_logging_level,
    configure_logging,
    get_configuration_file,
    get_ipc_file_path,
    get_runner,
    get_thonny_user_dir,
    get_version,
    prepare_thonny_user_dir,
)

logger = logging.getLogger(__name__)



