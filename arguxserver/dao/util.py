
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
__trigger_class = {
    "int" : IntSimpleTrigger,
    "float" : FloatSimpleTrigger,
    "text" : TextSimpleTrigger,
}

# Map
__alert_class = {
    "int" : IntSimpleAlert,
    "float" : FloatSimpleAlert,
    "text" : TextSimpleAlert,
}

# Map
__value_class = {
    "int" : IntValue,
    "float" : FloatValue,
    "text" : TextValue,
}
