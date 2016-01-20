"""
DAO Utility module.

Contains dictionaries for looking up the different Value types.
"""
from argux_server.models import (
    IntValue,
    IntSimpleTrigger,
    IntSimpleAlert,
    FloatValue,
    FloatSimpleTrigger,
    FloatSimpleAlert,
    TextValue,
    TextSimpleTrigger,
    TextSimpleAlert,
)

TRIGGER_CLASS = {
    "int": IntSimpleTrigger,
    "float": FloatSimpleTrigger,
    "text": TextSimpleTrigger,
}

ALERT_CLASS = {
    "int": IntSimpleAlert,
    "float": FloatSimpleAlert,
    "text": TextSimpleAlert,
}

VALUE_CLASS = {
    "int": IntValue,
    "float": FloatValue,
    "text": TextValue,
}
