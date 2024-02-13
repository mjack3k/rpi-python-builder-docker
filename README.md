# rpi-python-builder-docker
Docker image for building python for raspberry pi


## Current status
It is working, but is not automated properly yet


## What is this?
In short? A **docker image** to build python for RPI. 

### Long description
This is a system that will help you build a docker image with configured cross-compiler for your raspberry pi. 
You can use it as a base and expand for compiling different software, but the main goal is to provide python. 
It provides you various scripts to maximally simplify the process - a single command builder, that will output
compiled python.

## Why?
On linux, you are at the mercy of the distro maintainers when it comes to python. And debian (and derivatives)
are notorious for being "extremely stable" - which usually means you use older versions. 
In most cases it is not THAT huge of a problem, but certain software (*\*cough\** homeassistant *\*cough\**)
has pretty crazy requirements and demands newest possible version.

Luckily, python allows you to run your scripts/programs inside "virtualenv", so you don't need a system-wide
installation, you can have your system using python 3.9, and have 3.12 in a local directory, and use THAT python
to create virtual environment.

## How to
This assumes that you have docker installed and set up on your machine.
This also kinda assumes that you use linux, but I am pretty sure that it can be adapter to run in windows
- the building steps are linux-specific, once you run the container it doesn't matter what system it runs on

1. Prepare system
   - install docker, check if hello world image runs
2. Download/clone this repository
3. Build the image
4. Run the container
5. Wait until finished
6. If all went well, your freshly compiled python will be inside the "out" directory
7. Copy the directory into your raspberry pi os
8. Use for whatever you need
  - for example, create virtual environment
