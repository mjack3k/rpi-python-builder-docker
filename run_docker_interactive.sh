# Change to the project root
cd $(dirname $(realpath $0))

docker run -it --rm --name rpi-builder -v ./out:/app/out rpi-python-builder
