# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( EXTERNAL )
from swiftserialize import TextSerializer, YAMLSerializer

# IMPORTS ( ROS )
from ament_index_python.packages import get_package_share_directory


# WILDCARD SYMBOLS
__all__ = [
    "PACKAGE",
    "CONFIG",
    "CONSTRAINTS"
]


# FUNCTIONS
def read_config_file(path: str, serializer: TextSerializer) -> dict:
    with open(path, 'rb') as file:
        encoded = file.read()
    return serializer.decode(encoded)


# CONSTANTS
SERIALIZER:     TextSerializer = YAMLSerializer('utf-8')
PACKAGE:        str = get_package_share_directory("goddard_launch")
CONFIG:         dict = read_config_file("config/config.local.yaml", SERIALIZER)
CONSTRAINTS:    dict = read_config_file(f"{PACKAGE}/config/constraints.yaml", SERIALIZER)
