# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( STANDARD )
from dataclasses import dataclass, field
from typing import TypeVar, Set

# IMPORTS ( PACKAGE )
from src.launch import LaunchParameter
from src.constants import CONFIG, CONSTRAINTS


# TEMPLATING
T = TypeVar('T')


# WILDCARD SYMBOLS
__all__ = [
    "SimulateParameter",
    "ManipTypeParameter",
    "EoATTypeParameter",
    "RobotIPParameter",
    "WorkflowParameter"
]


# CLASSES
@dataclass(frozen=True)
class RobotIPParameter(LaunchParameter[str]):
    """The robot's IP address. Ignored for SIL conditions."""
    argument: str = CONFIG["ROBOT"]["IP-ADDRESS"]
    constraints: Set[str] = field(default_factory=lambda: CONSTRAINTS["IP-ADDRESSES"])


@dataclass(frozen=True)
class ManipTypeParameter(LaunchParameter[str]):
    """Determines the target arm  hardware (ex: ur3e)."""
    argument: str = CONFIG["ROBOT"]["MANIPULATOR"]
    constraints: Set[str] = field(default_factory=lambda: CONSTRAINTS["MANIPULATORS"])


@dataclass(frozen=True)
class EoATTypeParameter(LaunchParameter[str]):
    """Determines the target EoAT (End of Arm Tool) (ex: Robotiq 2F-85)."""
    argument: str = CONFIG["ROBOT"]["EOAT"]
    constraints: Set[str] = field(default_factory=lambda: CONSTRAINTS["EOATS"])


@dataclass(frozen=True)
class WorkflowParameter(LaunchParameter[str]):
    """Determines which workflow package to launch."""
    argument: str = CONFIG["PROGRAM"]["WORKFLOW"]
    constraints: Set[str] = field(default_factory=lambda: CONSTRAINTS["WORKFLOWS"])


@dataclass(frozen=True)
class SimulateParameter(LaunchParameter[bool]):
    """Flag for Hardware-In-Loop (HIL) vs Software-In-Loop (SIL)."""
    argument: bool = CONFIG["PROGRAM"]["SIMULATE"]
    constraints: Set[bool] = field(default_factory=lambda: [True, False])
