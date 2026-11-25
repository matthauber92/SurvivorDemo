"""Compatibility import for historical firearm migration scripts."""
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from Tools.Unreal.weapon_extension_helpers import *
