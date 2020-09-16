#!/usr/bin/env python3

import sys

ACTIONS_HEAD = """
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
"""

ACTIONS_TARGET="""
  {target_name}:
    name: {target_name}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - uses: actions/cache@v2
        id: cache-dl
        with:
          path: dl_target
          key: openwrt-dl-{target_name}-${{{{ hashFiles('modules') }}}}
      - name: Prepare download cache
        if: steps.cache-dl.outputs.cache-hit == 'true'
        run: mkdir -p gluon/openwrt/dl; mv dl_target/* gluon/openwrt/dl/; ls gluon/openwrt/dl
      - name: Get the version
        id: get_version
        run: echo ::set-output name=VERSION::${{GITHUB_REF/refs\/tags\//}}
      - name: Checkout submodules
        uses: textbook/git-checkout-submodule-action@master
      - name: Install Dependencies
        run: sudo actions/install-dependencies.sh
      - name: Build
        run: actions/run-build.sh {target_name}
      - name: Create cache to save
        if: steps.cache-dl.outputs.cache-hit != 'true'
        run: mkdir dl_target; mv gluon/openwrt/dl/* dl_target/; find dl_target/ -size +20M -delete
      - name: Archive build logs
        if: ${{{{ !cancelled() }}}}
        uses: actions/upload-artifact@v1
        with:
          name: ${{{{ steps.get_version.outputs.VERSION }}}}_{target_name}_logs
          path: gluon/openwrt/logs
      - name: Archive build output
        uses: actions/upload-artifact@v1
        with:
          name: ${{{{ steps.get_version.outputs.VERSION }}}}_{target_name}_output
          path: gluon/output
"""

output = ACTIONS_HEAD

for target in sys.stdin:
	output += ACTIONS_TARGET.format(target_name=target.strip())

print(output)
