#!/usr/bin/env bash


MINICONDA=Miniconda3-4.3.30


set -e
# set -v

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


case "$(uname -s)-$(uname -m)" in
    Darwin-x86_64)
	ARCH=MacOSX-x86_64 ;;
    Linux-x86_64)
	ARCH=Linux-x86_64 ;;
    Linux-i*)
	ARCH=Linux-x86 ;;
    *)
	echo 'Unknown architecture'
	exit 1
esac

DOWNLOAD_URL=https://repo.continuum.io/miniconda/$MINICONDA-$ARCH.sh

mkdir -p "$BOOTSTRAP"
"$BOOTSTRAP"/download.py "$BOOTSTRAP"/$MINICONDA.sh $DOWNLOAD_URL
rm -rf "$BOOTSTRAP"/miniconda
bash "$BOOTSTRAP"/$MINICONDA.sh -b -p "$BOOTSTRAP"/miniconda

"$BOOTSTRAP"/miniconda/bin/conda create -y -n bootstrap python=3 git pyyaml
