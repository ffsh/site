#!/usr/bin/env python3

import sys

ACTIONS_HEAD = """
# Update this file after adding/removing/renaming a target by running
# `make list-targets BROKEN=1 | ../actions/generate-actions.py > ../.github/workflows/build-gluon.yml`

name: Build Gluon
on:
  push:
    branches:
      - testing
      - rc
      - stable
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
"""

ACTIONS_TARGET="""
  {target_name}:
    name: {target_name}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - name: Checkout submodules
        uses: textbook/git-checkout-submodule-action@master
      - name: Install Dependencies
        run: sudo actions/install-dependencies.sh
      - name: Build
        run: actions/run-build.sh {target_name}
      - name: Archive build logs
        if: ${{{{ !cancelled() }}}}
        uses: actions/upload-artifact@v1
        with:
          name: {target_name}_logs
          path: gluon/openwrt/logs
      - name: Archive build output
        uses: actions/upload-artifact@v1
        with:
          name: {target_name}_output
          path: gluon/output
"""

output = ACTIONS_HEAD

for target in sys.stdin:
	output += ACTIONS_TARGET.format(target_name=target.strip())

print(output)