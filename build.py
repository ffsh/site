#!/usr/bin/python3
"""
Build script for Freifunk Suedholstein firmware runningn on Jenkins CI

Source: https://github.com/ffsh
Web: https://freifunk-suedholstein.de

"""
import argparse
import json
import os
import time
from datetime import datetime
from subprocess import call

DEFAULTS = {
    'targets' : ['ar71xx-generic', 'ar71xx-tiny', 'ar71xx-nand',
                 'brcm2708-bcm2708', 'brcm2708-bcm2709',
                 'mpc85xx-generic', 'ramips-mt7621',
                 'sunxi-cortexa7', 'x86-generic',
                 'x86-geode', 'x86-64 ramips-mt7620',
                 'ramips-mt76x8', 'ramips-rt305x'],
    'gluon_dir': '/gluon',
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
PARSER.add_argument("-d", metavar="Public Direcotry", dest="directory",
                    help="build.py -d /var/www/firmware (jenkins needs rw)", required=False)
PARSER.add_argument("--commit", metavar="Commit", dest="commit",
                    help="build.py --commit sha", required=True)

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
            call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                  "GLUON_SITEDIR="+ARGS.workspace,
                  "GLUON_TARGET="+target,
                  "clean"])
    else:
        call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
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
        all_targets = False
    except TypeError:
        all_targets = True

    if all_targets:
        for target in DEFAULTS["targets"]:
            print("Cleaning target: {}".format(target))
            call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                  "GLUON_SITEDIR="+ARGS.workspace,
                  "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], ARGS.branch,
                                                  ARGS.build_number),
                  "GLUON_BRANCH="+ARGS.branch,
                  "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
                  "GLUON_TARGET="+target,
                  "all"])
    else:
        print("Cleaning target: {}".format(target))
        call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
              "GLUON_SITEDIR="+ARGS.workspace,
              "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], ARGS.branch,
                                              ARGS.build_number),
              "GLUON_BRANCH="+ARGS.branch,
              "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
              "GLUON_TARGET="+target,
              "all"])
    print("Generating buid.json")
    time_stamp_sec = time.time()
    time_stamp = datetime.fromtimestamp(time_stamp_sec).strftime('%Y-%m-%d-%H-%M-%S')
    data = {
        'build_date' : time_stamp,
        'release' : "{}-{}-{}".format(DEFAULTS['release'], ARGS.branch,
                                      ARGS.build_number),
        'branch' : ARGS.branch,
        'commit' : ARGS.commit
    }
    with open("{}/output/images/build.json".format(ARGS.workspace), "w") as file:
        json.dumps(data, file)

    # Create manifest
    print("Createing Manifest ...")
    call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
          "GLUON_SITEDIR="+ARGS.workspace,
          "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], ARGS.branch,
                                          ARGS.build_number),
          "GLUON_BRANCH="+ARGS.branch,
          "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
          "GLUON_TARGET="+target,
          "manifest"])

def sign():
    """
    Signs the manifest
    """
    pass

def publish():
    """
    Copy the images to a public directory
    """
    try:
        directory = str(ARGS.directory)
    except ValueError:
        raise ValueError("You need to provide a valid path eg. -d /var/www/firmware")
    if os.path.isdir(directory):
        # direcotry/BRANCH/build.json
        if os.path.isdir("{}/{}".format(directory, ARGS.branch)):

            print("Detected old builds move to archive")
            dir_source = "{}/{}".format(directory, ARGS.branch)

            with open(dir_source+"/build.json") as file:
                old_build_date = json.load(file)["build_date"]
            dir_target = "{}/archive/{}-{}".format(directory, ARGS.branch, old_build_date)

            call(["cp", "-r", dir_source, dir_target])

        dir_source = "{}/output/images".format(ARGS.workspace)
        dir_target = "{}/{}".format(directory, ARGS.branch)
        call(["cp", "-rL", dir_source, dir_target])
    else:
        raise ValueError("{} Path does not exist!".format(directory))

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
