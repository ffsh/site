#!/bin/sh

set -e

export GLUON_RELEASE=gluon-ffsh-2020.1.2.0


export BROKEN=0
export GLUON_AUTOREMOVE=1
export GLUON_DEPRECATED ?= upgrade
export GLUON_SITEDIR="../"
export GLUON_TARGET=$1
export BUILD_LOG=1

cd gluon/

make update
make -j2
