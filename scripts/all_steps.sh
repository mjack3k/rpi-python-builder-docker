#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd SCRIPT_DIR

# Download
bash dl_python.sh

# Build for build-pc
bash build_for_buildpc.sh

# Build final python for rpi
bash build_python.sh
