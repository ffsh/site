#!/bin/sh

set -e

apt-get -y update
apt-get -y install git subversion build-essential python3 python3-pyelftools gawk unzip libncurses-dev zlib1g-dev libssl-dev wget time qemu-utils libelf-dev clang llvm pkg-config rsync gettext file patch device-tree-compiler python3-yaml
apt-get -y clean
rm -rf /var/lib/apt/lists/*
