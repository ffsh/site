#!/bin/sh

set -e

export BROKEN=1
export GLUON_AUTOREMOVE=1
export GLUON_DEPRECATED=1
export GLUON_SITEDIR="../"
export GLUON_TARGET=$1
export BUILD_LOG=1

cd gluon/

make update
make -j2
