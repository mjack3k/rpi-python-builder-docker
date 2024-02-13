# Script for building docker image

# Change to the project root
cd $(dirname $(realpath $0))

docker build --rm -t rpi-python-builder .

# Remove unused images (is it always safe to do so?)
docker image prune -f


