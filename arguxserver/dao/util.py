
from arguxserver.models import (
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

# Map
TRIGGER_CLASS = {
    "int" : IntSimpleTrigger,
    "float" : FloatSimpleTrigger,
    "text" : TextSimpleTrigger,
}

# Map
ALERT_CLASS = {
    "int" : IntSimpleAlert,
    "float" : FloatSimpleAlert,
    "text" : TextSimpleAlert,
}

# Map
VALUE_CLASS = {
    "int" : IntValue,
    "float" : FloatValue,
    "text" : TextValue,
}
