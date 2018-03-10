#!/usr/bin/python3
"""
Build script for Freifunk Suedholstein firmware runningn on Jenkins CI

Source: https://github.com/ffsh
Web: https://freifunk-suedholstein.de

"""
import argparse
import json
from subprocess import call

DEFAULTS = {
    'targets' : ['ar71xx-generic', 'ar71xx-tiny', 'ar71xx-nand',
                 'brcm2708-bcm2708', 'brcm2708-bcm2709',
                 'mpc85xx-generic', 'ramips-mt7621',
                 'sunxi-cortexa7', 'x86-generic',
                 'x86-geode', 'x86-64 ramips-mt7620',
                 'ramips-mt76x8', 'ramips-rt305x'],
    'gluon_dir': '/home/grotax/git/site-ffsh/gluon',
    'makeopts' : 'V=s -j$(expr $(nproc) + 1)',
    'release': '2018.1',
    'priority': 1
}

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-c", metavar="Command", dest="command",
                    help="build.py -c clean | update | build | sign | publish", required=True)
PARSER.add_argument("-b", metavar="Branch", dest="branch",
                    help="build.py -b dev | testing | rc | stable", required=True)
PARSER.add_argument("-w", metavar="Workspace", dest="workspace",
                    help="build.py -w \"${WORKSPACE}\"", required=True)
PARSER.add_argument("-n", metavar="Build Number", dest="build_number",
                    help="build.py -n ${BUILD_NUMBER}", required=True)
PARSER.add_argument("-t", metavar="Target", dest="target",
                    help="build.py -t ar71xx-generic | ...", required=False)

ARGS = PARSER.parse_args()


def clean():
    """
    Cleans the output Directory. Not necessary!
    """
    try:
        target = str(ARGS.target)
        print(target+" "+type(target))
        all_targets = False
    except TypeError:
        all_targets = True

    if all_targets:
        for target in DEFAULTS["targets"]:
            print("Cleaning target: {}".format(target))
            call(["make", "-C", DEFAULTS['gluon_dir'],
                  "GLUON_SITEDIR="+ARGS.workspace,
                  "GLUON_TARGET="+target,
                  "clean"])
    else:
        call(["make", "-C", DEFAULTS['gluon_dir'],
              "GLUON_SITEDIR="+ARGS.workspace,
              "GLUON_TARGET="+target,
              "clean"])

def update():
    """
    Updates the repository
    """
    call(["make", "-C", DEFAULTS['gluon_dir'],
          "GLUON_SITEDIR="+ARGS.workspace,
          "update"])


def build():
    """
    Build images definded by -t or default targets
    """
    try:
        target = str(ARGS.target)
        print(target+" "+type(target))
        all_targets = False
    except TypeError:
        all_targets = True

    if all_targets:
        for target in DEFAULTS["targets"]:
            print("Cleaning target: {}".format(target))
            call(["make", "-C", DEFAULTS['gluon_dir'],
                  "GLUON_SITEDIR="+ARGS.workspace,
                  "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], ARGS.branch,
                                                  ARGS.build_number),
                  "GLUON_BRANCH="+ARGS.branch,
                  "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
                  "GLUON_TARGET="+target,
                  "all"])
    else:
        call(["make", "-C", DEFAULTS['gluon_dir'],
              "GLUON_SITEDIR="+ARGS.workspace,
              "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], ARGS.branch,
                                              ARGS.build_number),
              "GLUON_BRANCH="+ARGS.branch,
              "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
              "GLUON_TARGET="+target,
              "all"])

def sign():
    """
    Signs the manifest
    """
    pass

def publish():
    """
    Copy the images to a public directory
    """
    pass

def main():
    """
    Entry function
    """
    with open(ARGS.workspace + '/release.json', 'r') as file:
        global DEFAULTS
        data = json.load(file)
        DEFAULTS['release'] = data['version']
        DEFAULTS['priority'] = data['priority']


    if ARGS.command == "clean":
        clean()
    elif ARGS.command == "update":
        update()
    elif ARGS.command == "build":
        build()
    elif ARGS.command == "sign":
        sign()
    elif ARGS.command == "publish":
        publish()
    else:
        raise ValueError("Command can only be one of: clean | update | build | sign | publish")


if __name__ == '__main__':
    main()
