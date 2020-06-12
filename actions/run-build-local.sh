#!/bin/sh

set -e

export GLUON_RELEASE=2020.1.2.0


export BROKEN=0
export GLUON_AUTOREMOVE=0
export GLUON_DEPRECATED=upgrade
export GLUON_SITEDIR="../"
export BUILD_LOG=1

cd gluon/

#make update

for TARGET in $(make list-targets); do
    make -j13 GLUON_TARGET=$TARGET
done