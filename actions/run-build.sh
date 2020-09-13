#!/bin/sh

set -e

export GLUON_RELEASE=2020.1.3.0


export BROKEN=0
export GLUON_AUTOREMOVE=1
export GLUON_DEPRECATED=upgrade
export GLUON_SITEDIR="../"
export GLUON_TARGET=$1
export BUILD_LOG=1

# needed for manifest
export GLUON_BRANCH="master"
export GLUON_PRIORITY=1

cd gluon/

make update
make -j2
make manifest
