#!/bin/sh

set -e

export GLUON_RELEASE=2021.0.0.0-w


export BROKEN=0
export GLUON_AUTOREMOVE=0
export GLUON_DEPRECATED=upgrade
export GLUON_SITEDIR="../"
export BUILD_LOG=1

cd gluon/

make update

make -j1 V=s GLUON_TARGET=ar71xx-generic

#for TARGET in $(make list-targets); do
#    make -j1 V=s GLUON_TARGET=$TARGET
#done