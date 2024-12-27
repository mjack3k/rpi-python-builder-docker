# rpi-python-builder-docker
Docker image for building python for raspberry pi
<br>

## Current status
You can use the individual scripts to build python manually, or alternatively use the provided GUI.
<br>

## What is this?
In short? A **docker image** to build python for RPI. 
<br>

### Long description
This is a system that will help you build a docker image with configured cross-compiler for your raspberry pi. 
You can use it as a base and expand for compiling different software, but the main goal is to provide python. 
It provides you various scripts to maximally simplify the process - a single command builder, that will output
compiled python.
<br>

## Why?
On linux, you are at the mercy of the distro maintainers when it comes to python. And debian (and derivatives)
are notorious for being "extremely stable" - which usually means you use older versions. 
In most cases it is not THAT huge of a problem, but certain software (*\*cough\** homeassistant *\*cough\**)
has pretty crazy requirements and demands newest possible version.
<br>
Luckily, python allows you to run your scripts/programs inside "virtualenv", so you don't need a system-wide
installation, you can have your system using python 3.9, and have 3.12 in a local directory, and use THAT python
to create virtual environment.
<br>

## How to
This assumes that you have docker installed and set up on your machine.
This also kinda assumes that you use linux, but I am pretty sure that it can be adapter to run in windows
- the building steps are linux-specific, once you run the container it doesn't matter what system it runs on

### Using the provided GUI
1. Prepare system
   - install docker, check if hello world image runs
2. Download/clone this repository
3. Install python3 and modules (on windows - inside WSL)
   `sudo apt install python3-tk python3-paramiko`
4. Run the GUI (on windows - from WSL)
   `python3 start_gui.py`
5. Enter your Raspberry Pi credentials
   Username, host/IP address, port
6. Use the buttons on the right to build and install
   - start with building docker image
   - then build python - this step takes a long time
   - install - this will pack the Python and copy over SSH to your RPI
   
   Status widget below shows you, if the docker image is available, and if the produced python directory exists. 

### Manual build
1. Prepare system
   - install docker, check if hello world image runs
2. Download/clone this repository
3. Build the image
   - just call `build_docker.sh`
4. Run the container
   - right now you need to run in interactive mode
   - run `run_docker_interactive.sh`
5. Build
   - Inside docker container, run `dl_python.sh`
   - run `build_for_buildpc.sh`
   - run `build_python.sh`
   - `exit`
6. If all went well, your freshly compiled python will be inside the "out" directory
7. You can pack your python to create tarball
   - for example: `tar czvf python.tgz PYTHON_3.12.2`
8. Copy the directory into your raspberry pi os
   - for example `scp python.tgz pi@YOUR_RPI_IP:/home/pi/
10. Use for whatever you need
  - unpack, run the binary inside the freshly unpacked directory (python/3.12.2/bin/python3)
  - create venv: ./python3 -m venv /srv/homeassistant/
