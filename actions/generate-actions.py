#!/usr/bin/env python3

import sys

ACTIONS = r"""
# Update this file after adding/removing/renaming a target by running the script from gluon dir
# `make list-targets BROKEN=0 GLUON_DEPRECATED=upgrade GLUON_SITEDIR="../"| ../actions/generate-actions.py > ../.github/workflows/build-gluon.yml`

name: Build Gluon
on:
  push:
    tags:
      - 2021.*
      - 2022.*
      - 2023.*
jobs:
  build_firmware:
    strategy:
      fail-fast: false
      matrix:
        target: [{matrix}]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      - name: Get the version
        id: get_version
        run: echo "VERSION=${{GITHUB_REF/refs\/tags\//}}" >> $GITHUB_ENV
      - name: Install Dependencies
        run: sudo actions/install-dependencies.sh
      - name: Build
        run: actions/run-build.sh ${{{{matrix.target}}}}
      - name: Archive build output
        uses: actions/upload-artifact@v4
        with:
          name: ${{{{ env.VERSION }}}}_${{{{matrix.target}}}}_output
          path: gluon/output
"""

targets = [target.strip() for target in sys.stdin]


output = ACTIONS.format(matrix=", ".join(targets))

print(output)
