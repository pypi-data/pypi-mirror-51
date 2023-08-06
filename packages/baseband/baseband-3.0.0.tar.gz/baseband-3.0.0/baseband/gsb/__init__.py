# Licensed under the GPLv3 - see LICENSE
"""GMRT Software Backend (GSB) data reader.

See http://gmrt.ncra.tifr.res.in/gmrt_hpage/sub_system/gmrt_gsb/index.htm
"""
from .base import open
from .header import GSBHeader
from .payload import GSBPayload
from .frame import GSBFrame
