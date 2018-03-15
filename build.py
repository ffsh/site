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
    'priority': 1,
    'branch': 'dev'
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
PARSER.add_argument("-s", metavar="Secret", dest="secret",
                    help="build.py -s <path to secret>", required=False)
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
    call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
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
                  "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], DEFAULTS['branch'],
                                                  ARGS.build_number),
                  "GLUON_BRANCH="+DEFAULTS['branch'],
                  "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
                  "GLUON_TARGET="+target,
                  "all"])
    else:
        print("Cleaning target: {}".format(target))
        call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
              "GLUON_SITEDIR="+ARGS.workspace,
              "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], DEFAULTS['branch'],
                                              ARGS.build_number),
              "GLUON_BRANCH="+DEFAULTS['branch'],
              "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
              "GLUON_TARGET="+target,
              "all"])
    print("Generating buid.json")
    time_stamp_sec = time.time()
    time_stamp = datetime.fromtimestamp(time_stamp_sec).strftime('%Y-%m-%d-%H-%M-%S')
    data = {
        'build_date' : time_stamp,
        'release' : "{}-{}-{}".format(DEFAULTS['release'], DEFAULTS['branch'],
                                      ARGS.build_number),
        'branch' : DEFAULTS['branch'],
        'commit' : ARGS.commit
    }
    with open("{}/output/images/build.json".format(ARGS.workspace), "w") as file:
        json.dump(data, file)

    # Create manifest
    print("Createing Manifest ...")

    if not os.path.isdir("{}/tmp/origin/".format(ARGS.workspace)):
        # Make sure that the tmp dir exists
        call(["mkdir", "-p", "{}/tmp/origin/".format(ARGS.workspace)])

    call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
          "GLUON_SITEDIR="+ARGS.workspace,
          "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], DEFAULTS['branch'],
                                          ARGS.build_number),
          "GLUON_BRANCH="+DEFAULTS['branch'],
          "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
          "GLUON_TARGET="+target,
          "manifest"])

def sign():
    """
    Signs the manifest
    """
    call(["{}/contrib/sign.sh".format(ARGS.workspace), ARGS.secret,
          "{}/output/images/sysupgrade/{}.manifest".format(ARGS.workspace, DEFAULTS['branch'])])

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
        if os.path.isdir("{}/{}".format(directory, DEFAULTS['branch'])):

            print("Detected old builds move to archive")
            dir_source = "{}/{}".format(directory, DEFAULTS['branch'])

            with open(dir_source+"/build.json") as file:
                old_build_date = json.load(file)["build_date"]
            dir_target = "{}/archive/{}-{}".format(directory, DEFAULTS['branch'], old_build_date)

            call(["cp", "-r", dir_source, dir_target])

        dir_source = "{}/output/images".format(ARGS.workspace)
        dir_target = "{}/{}".format(directory, DEFAULTS['branch'])
        call(["cp", "-rL", dir_source, dir_target])
    else:
        raise ValueError("{} Path does not exist!".format(directory))

def main():
    """
    Entry function
    """
    global DEFAULTS
    with open(ARGS.workspace + '/release.json', 'r') as file:
        data = json.load(file)
        DEFAULTS['release'] = data['version']
        DEFAULTS['priority'] = data['priority']

    if "/" in ARGS.branch:
        DEFAULTS['branch'] = ARGS.branch.split("/")[1]
        print("Warning: found \"/\" in branch name, changing to: {}".format(DEFAULTS['branch']))

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
