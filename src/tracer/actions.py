"""Definitions of the three TRACER routing actions."""

from enum import StrEnum


class Action(StrEnum):
    """An action available after a small language model produces a response."""

    ACCEPT = "accept"
    REPAIR = "repair"
    REGENERATE = "regenerate"


ACTION_DEFINITIONS = {
    Action.ACCEPT: (
        "Return the original small-model response without changing its substantive content."
    ),
    Action.REPAIR: (
        "Give the original response and external validator evidence to a stronger model, "
        "asking it to preserve valid content while correcting detected defects."
    ),
    Action.REGENERATE: (
        "Discard the original response and ask a stronger model to solve the original task "
        "from scratch."
    ),
}

