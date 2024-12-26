# Change to the project root
cd $(dirname $(realpath $0))

docker run --rm --name rpi-builder -v ./out:/app/out rpi-python-builder
