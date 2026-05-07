#!/bin/bash

# Provides simple named colors for terminal printing

# CONSTANTS
RESET=$(tput sgr0)
RED=$(tput setaf 196)
ORANGE=$(tput setaf 173)
YELLOW=$(tput setaf 11)
GREEN=$(tput setaf 70)
BLUE=$(tput setaf 33)
PURPLE=$(tput setaf 99)

# FUNCTIONS
paint() {
    local color="$1"
    shift
    local message="$*"
    echo -e "${color}${message}${RESET}"
}