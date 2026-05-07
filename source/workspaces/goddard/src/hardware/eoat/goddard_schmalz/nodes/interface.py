# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( STANDARD )
from abc import ABC as Abstract
from abc import abstractmethod
from typing import TYPE_CHECKING

# IMPORTS ( PACKAGE )
if TYPE_CHECKING:
    from controller import SchmalzController


# CLASSES
class SchmalzControlInterface(Abstract):

    # INTRINSIC METHODS
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
    
    # ABSTRACT METHODS
    @abstractmethod
    def connect(self, timeout: float):
        ...

    @abstractmethod
    def activate(self) -> bool:
        ...

    @abstractmethod
    def deactivate(self) -> bool:
        ...
