#!/bin/sh

set -e

# Change this to give your build a different version
export GLUON_RELEASE=2022.1.0.0

# Don't change these
export BROKEN=0
export GLUON_AUTOREMOVE=0
export GLUON_DEPRECATED=upgrade
export GLUON_SITEDIR="../"
export BUILD_LOG=1

cd gluon/

# Optional dirclean can help to fix certain build issues, rm -rf gluon, is more effective in my mind
#make dirclean

# Updates the dependencies of gluon
make update

# adjust -j to build with more cores
# adjust GLUON_TARGET to build a different Target
make -j1 V=s GLUON_TARGET=ath79-generic

#for TARGET in $(make list-targets); do
#    make -j1 V=s GLUON_TARGET=$TARGET
#done