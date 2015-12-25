"""Utility module containing regular expressions."""

import re

TIME_OFFSET_EXPR = re.compile(r"([-+])([0-9]+)([mhd])")
TIMESPAN_EXPR    = re.compile(r"([0-9]+)([mhd])")

TRIGGER_EXPR = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?(?:[0-9]+(?:[\.,][0-9]+)?))")

DATE_FMT = "%Y-%m-%dT%H:%M:%S"

