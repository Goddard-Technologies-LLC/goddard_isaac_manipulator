# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( STANDARD )
from enum import Enum, auto


# CLASSES
class RuntimeState(Enum):
    """Indicates the overall operational state of the robotic system."""
    
    # Generic
    IDLE    = auto()
    NORMAL  = auto()
    FAULT   = auto()
    PAUSED  = auto()

    # Elevated states
    CAUTION = auto() # slow zones etc.
    WARNING = auto()
    ERROR   = auto()

    # Motion Planning
    NO_PATH     = auto()
    COLLISION   = auto()
