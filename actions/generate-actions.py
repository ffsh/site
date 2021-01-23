#!/usr/bin/env python3

import sys

ACTIONS = """
# Update this file after adding/removing/renaming a target by running the script from gluon dir
# `make list-targets BROKEN=0 GLUON_DEPRECATED=upgrade GLUON_SITEDIR="../"| ../actions/generate-actions.py > ../.github/workflows/build-gluon.yml`

name: Build Gluon
on:
  push:
    tags:
      - 2020.*
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  build_firmware:
    strategy:
      fail-fast: false
      matrix:
        target: [{matrix}]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - name: Get the version
        id: get_version
        run: echo ::set-output name=VERSION::${{GITHUB_REF/refs\/tags\//}}
      - name: Checkout submodules
        uses: textbook/git-checkout-submodule-action@master
      - name: Install Dependencies
        run: sudo actions/install-dependencies.sh
      - name: Build
        run: actions/run-build.sh ${{{{matrix.target}}}}
      - name: Archive build logs
        if: ${{{{ !cancelled() }}}}
        uses: actions/upload-artifact@v1
        with:
          name: ${{{{ steps.get_version.outputs.VERSION }}}}_${{{{matrix.target}}}}_logs
          path: gluon/openwrt/logs
      - name: Archive build output
        uses: actions/upload-artifact@v1
        with:
          name: ${{{{ steps.get_version.outputs.VERSION }}}}_${{{{matrix.target}}}}_output
          path: gluon/output
"""

targets = [target.strip() for target in sys.stdin]


output = ACTIONS.format(matrix=", ".join(targets))

print(output)
