#!/usr/bin/env bash

MINICONDA_32=Miniconda3-4.5.12
MINICONDA_64=Miniconda3-py38_4.8.3


case "$(uname -s)-$(uname -m)" in
    Darwin-x86_64)
        MINICONDA=$MINICONDA_64
        ARCH=macOS-x86_64 ;;
    Linux-x86_64)
        MINICONDA=$MINICONDA_64
        ARCH=Linux-x86_64 ;;
    Linux-i*)
        MINICONDA=$MINICONDA_32
        ARCH=Linux-x86 ;;
    *)
        echo 'Unknown architecture'
        exit 1
esac


set -e
# set -v

# Find a python binary
PYTHON2=$(which python) || true
PYTHON3=$(which python3) || true
if [ -n "$PYTHON2" ] ; then 
    PYTHON=$PYTHON2
else
    PYTHON=$PYTHON3
fi


# This is the root dir
DIR="$(pwd)"
if [ -x "$DIR/binary_pkg" ] ; then
    echo "Root directory = $DIR"
else
    echo "binary_pkg not found in root directory $DIR"
    exit 1
fi

export BOOTSTRAP="$DIR/tools/bootstrap"

if [ -d "$BOOTSTRAP"/miniconda/envs/bootstrap ]; then
    echo "Bootstrap already installed"
    exit 0
fi


DOWNLOAD_URL=https://repo.anaconda.com/miniconda/$MINICONDA-$ARCH.sh

mkdir -p "$BOOTSTRAP"
$PYTHON "$BOOTSTRAP"/download.py "$BOOTSTRAP"/$MINICONDA.sh $DOWNLOAD_URL
rm -rf "$BOOTSTRAP"/miniconda
bash "$BOOTSTRAP"/$MINICONDA.sh -b -p "$BOOTSTRAP"/miniconda

"$BOOTSTRAP"/miniconda/bin/conda create -y -n bootstrap python=3 git pyyaml
