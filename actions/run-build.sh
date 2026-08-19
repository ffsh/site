#!/bin/sh

set -e

export GLUON_RELEASE=2025.1.3.0


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

# Check if target should be built in debug mode
if [ -f ../debug_targets.txt ] && grep -qx "$GLUON_TARGET" ../debug_targets.txt; then
    # Debug mode: single job with verbose output
    make GLUON_TARGET="$GLUON_TARGET" -j1 V=s
else
    # Normal mode: parallel build with nproc
    make GLUON_TARGET="$GLUON_TARGET" -j"$(nproc)"
fi

make manifest
