# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( STANDARD )-
from dataclasses import dataclass, fields
from typing import TypeVar, Generic, Set


# TEMPLATING
T = TypeVar('T')


# WILDCARD SYMBOLS
__all__ = [
    "LaunchParameter",
    "LaunchDefinition"
]


# CLASSES
@dataclass(frozen=True)
class LaunchParameter(Generic[T]):
    """Wraps a launch argument with a set of constraints."""
    argument: T
    constraints: Set[T]

    # INTRINSIC METHODS
    def __post_init__(self):
        if not self.validate():
            error = f"arg '{self.argument}' is not within defined constraints: {self.constraints}"
            raise ValueError(error)

    # PUBLIC METHODS
    def validate(self) -> bool:
        """Checks whether the argument is within the allowable constraints."""
        return self.argument in self.constraints


@dataclass(frozen=True)
class LaunchDefinition:
    """Contains the set of arguments used to define the program's overall
    composition and runtime behavior."""
    robot_ip:       LaunchParameter[str]
    manipulator:    LaunchParameter[str]
    eoat:           LaunchParameter[str]
    workflow:       LaunchParameter[str]
    simulate:       LaunchParameter[bool]

    # INTRINSIC METHODS
    def __repr__(self):
        attr_strs = []
        for field in fields(self):
            val: T = getattr(self, field.name)
            attr_strs.append(f"{field.name}={val.argument!r}")
        return f"{self.__class__.__name__}({', '.join(attr_strs)})"
