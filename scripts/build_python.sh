# Set python version
export PYTHON_VERSION=3.12.2
export PYTHON_MAJOR=3

# Set install dir
OUTDIR=/app/out/PYTHON_${PYTHON_VERSION}

# Prepare clean build dir
rm -rf Python-${PYTHON_VERSION}
tar xvf Python-${PYTHON_VERSION}.tgz

# Goto source dir
cd Python-${PYTHON_VERSION}

CONFIG_SITE=/app/config.site-rpi ./configure \
    --prefix=${OUTDIR}/${PYTHON_VERSION} \
    --build=x86_64-pc-linux-gnu \
    --host=arm-linux-gnueabihf \
    --enable-ipv6 \
    --with-build-python=/app/python_local/${PYTHON_VERSION}/bin/python3 \
    --with-ensurepip=install
make -j6
make install
