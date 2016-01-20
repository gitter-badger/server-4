"""Utility module containing regular expressions."""

import re

TIME_OFFSET_EXPR = re.compile(r"([-+])([0-9]+)([mhd])")

TIMESPAN_EXPR = re.compile(r"([0-9]+)([mhdM])")

"""Regular expression matching trigger names.

selector(<number>) compare [number]

These trigger rules only make sense for integer
and floating-point numbers.
"""
TRIGGER_EXPR = re.compile(
    r"([a-z]+)"
    r"\(([0-9]*)\)"
    r"[ ]*"
    r"(>|<|>=|<=|==|!=)"
    r"[ ]*"
    r"([-]?(?:[0-9]+(?:[\.,][0-9]+)?))")

DATE_FMT = "%Y-%m-%dT%H:%M:%S"

USERNAME_EXPR = re.compile(
    r"((?:([A-Z])+[/])?"
    r"([a-z]+))")
