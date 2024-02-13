# Use Alpine as the base image
FROM debian:latest

# Set environment variables for cross-compilation
ENV CC=arm-linux-gnueabihf-gcc
ENV CXX=arm-linux-gnueabihf-g++
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary tools and libraries
## Add armhf arch support
RUN dpkg --add-architecture armhf
RUN apt update
RUN apt -y upgrade
RUN apt -y install build-essential ca-certificates curl g++ gcc \
    gcc-arm-linux-gnueabihf libbz2-dev libdb-dev libffi-dev libgdbm-dev \
    liblzma-dev libncurses-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
    libssl-dev libssl-dev libxml2-dev libxmlsec1-dev nano tk-dev uuid-dev \
    wget xz-utils zlib1g-dev

### Install libraries for armhf (raspberry pi arch)
RUN apt -y install libbz2-dev:armhf libdb-dev:armhf libffi-dev:armhf \ 
    libgdbm-dev:armhf liblzma-dev:armhf libncurses-dev:armhf \
    libncursesw5-dev:armhf libreadline-dev:armhf libsqlite3-dev:armhf \
    libssl-dev:armhf libssl-dev:armhf libxml2-dev:armhf libxmlsec1-dev:armhf \
    tk-dev:armhf uuid-dev:armhf zlib1g-dev:armhf
RUN apt clean

# Delete index files we don't need anymore:
RUN rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a shared for output directory
RUN mkdir /app/out

# Copy scripts
COPY ./scripts /app

