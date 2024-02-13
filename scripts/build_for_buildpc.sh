# Set python version
export PYTHON_VERSION=3.12.2
export PYTHON_MAJOR=3

# Disable the env variables for x86_64 build
CC=""
CXX=""

# Set install dir
OUTDIR=/app/shared/python

# Goto source dir
cd Python-${PYTHON_VERSION}

./configure \
    --prefix=/app/python_local/${PYTHON_VERSION} \
    --enable-ipv6
make -j6
make install
