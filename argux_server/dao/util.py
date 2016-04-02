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
    BooleanValue,
    BooleanSimpleTrigger,
    BooleanSimpleAlert,
)

TRIGGER_CLASS = {
    "int": IntSimpleTrigger,
    "float": FloatSimpleTrigger,
    "text": TextSimpleTrigger,
    "boolean": BooleanSimpleTrigger,
}

ALERT_CLASS = {
    "int": IntSimpleAlert,
    "float": FloatSimpleAlert,
    "text": TextSimpleAlert,
    "boolean": BooleanSimpleAlert,
}

VALUE_CLASS = {
    "int": IntValue,
    "float": FloatValue,
    "text": TextValue,
    "boolean": BooleanValue,
}
