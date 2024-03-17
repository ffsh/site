#!/bin/sh

set -e

export GLUON_RELEASE=2023.2.2.0


export BROKEN=0
export GLUON_AUTOREMOVE=1
export GLUON_DEPRECATED=upgrade
export GLUON_SITEDIR="../"
export GLUON_TARGET=$1
export BUILD_LOG=1

# needed for manifest and actually the autoupdater
export GLUON_AUTOUPDATER_BRANCH=stable
export GLUON_AUTOUPDATER_ENABLED=1
export GLUON_PRIORITY=0

cd gluon/

make update
# https://github.blog/2024-01-17-github-hosted-runners-double-the-power-for-open-source/
make -j4
make manifest
