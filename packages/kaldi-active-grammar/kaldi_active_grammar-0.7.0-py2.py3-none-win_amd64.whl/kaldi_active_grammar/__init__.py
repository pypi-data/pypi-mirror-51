#
# This file is part of kaldi-active-grammar.
# (c) Copyright 2019 by David Zurow
# Licensed under the AGPL-3.0, with exceptions; see LICENSE.txt file.
#

_name = 'kaldi_active_grammar'
__version__ = '0.7.0'
REQUIRED_MODEL_VERSION = '0.5.0'
DEFAULT_MODEL_DIR = 'kaldi_model_zamia'
DEFAULT_TMP_DIR_SUFFIX = '.tmp'

import logging
_log = logging.getLogger('kaldi')

class KaldiError(Exception):
    pass

from .utils import FileCache
from .wfst import WFST
from .compiler import Compiler, KaldiRule
from .wrapper import KaldiAgfNNet3Decoder
from .model import Model
