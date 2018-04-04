#!/usr/bin/python3
"""
Build script for Freifunk Suedholstein firmware runningn on Jenkins CI

Source: https://github.com/ffsh/site
Web: https://freifunk-suedholstein.de

"""
import argparse
import json
import os
import time
from datetime import datetime
import subprocess as sp
# 'brcm2708-bcm2708', 'brcm2708-bcm2709', 'ramips-rt305x', 'sunxi-cortexa7'

DEFAULTS = {
    'targets' : ['ar71xx-generic', 'ar71xx-tiny', 'ar71xx-nand',
                 'mpc85xx-generic', 'ramips-mt7621', 'x86-generic',
                 'x86-geode', 'x86-64', 'ramips-mt7620',
                 'ramips-mt76x8'],
    'gluon_dir': '/gluon',
    'make_cores' : "1",
    'make_loglevel': 'V=s',
    'release': '2018.1',
    'priority': 1,
    'branch': 'dev'
}

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-c", metavar="Command", dest="command",
                    help="build.py -c clean | dirclean | update | build | sign | publish",
                    required=True)
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
PARSER.add_argument("--cores", metavar="Cores", dest="cores",
                    help="build.py --cores 4", required=False)
PARSER.add_argument("--log", metavar="Log Level", dest="log",
                    help="build.py --log V=s (stdout+stderr) | V=w (warnings/errors)",
                    required=False)


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
            sp.check_call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                           "GLUON_SITEDIR="+ARGS.workspace,
                           "GLUON_TARGET="+target,
                           "clean"])
    else:
        sp.check_call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                       "GLUON_SITEDIR="+ARGS.workspace,
                       "GLUON_TARGET="+target,
                       "clean"])

def dirclean():
    """
    Clean with dirclean
    """
    print("Starting dirclean ...")
    sp.check_call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                   "GLUON_SITEDIR="+ARGS.workspace,
                   "dirclean"])
    print("dirclean done.")

def update():
    """
    Updates the repository
    """
    print("Starting update ...")
    sp.check_call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                   "GLUON_SITEDIR="+ARGS.workspace,
                   "update"])
    print("Update done.")


def build():
    """
    Build images definded by -t or default targets
    """
    print("Info: Starting building ...")
    print("Info: delete OLD images in workdir...")
    dir_source = "{}/output/images/".format(ARGS.workspace)
    sp.check_call(["rm", "-rf", dir_source])
    build_errors = {
        "number": 0,
        "errors": []
    }
    if ARGS.target is not None:
        all_targets = False
        target = str(ARGS.target)
        print("Info: single target found")
    else:
        all_targets = True
        print("Info: build all Targets")

    if all_targets:
        for target in DEFAULTS["targets"]:
            print("Info: Building target: {}".format(target))
            try:
                sp.check_call(["make", "-j", DEFAULTS['make_cores'], "-C",
                               ARGS.workspace+DEFAULTS['gluon_dir'],
                               DEFAULTS['make_loglevel'],
                               "GLUON_SITEDIR="+ARGS.workspace,
                               "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'],
                                                               DEFAULTS['branch'],
                                                               ARGS.build_number),
                               "GLUON_BRANCH="+DEFAULTS['branch'],
                               "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
                               "GLUON_TARGET="+target,
                               "all"])
            except sp.CalledProcessError as process_error:
                print(process_error)
                build_errors["errors"].append(process_error)
                build_errors["number"] += 1

    else:
        print("Info: Building target: {}".format(target))
        sp.check_call(["make", "-j", DEFAULTS['make_cores'], "-C",
                       ARGS.workspace+DEFAULTS['gluon_dir'],
                       DEFAULTS['make_loglevel'],
                       "GLUON_SITEDIR="+ARGS.workspace,
                       "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], DEFAULTS['branch'],
                                                       ARGS.build_number),
                       "GLUON_BRANCH="+DEFAULTS['branch'],
                       "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
                       "GLUON_TARGET="+target,
                       "all"])

    print("Info: Generating buid.json")
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
        sp.check_call(["mkdir", "-p", "{}/tmp/origin/".format(ARGS.workspace)])

    sp.check_call(["make", "-C", ARGS.workspace+DEFAULTS['gluon_dir'],
                   "GLUON_SITEDIR="+ARGS.workspace,
                   "GLUON_RELEASE={}-{}-{}".format(DEFAULTS['release'], DEFAULTS['branch'],
                                                   ARGS.build_number),
                   "GLUON_BRANCH="+DEFAULTS['branch'],
                   "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
                   "GLUON_TARGET="+target,
                   "manifest"])
    if build_errors["number"] > 0:
        print("=============================")
        print("Error: We have {} Build errors".format(build_errors["number"]))
        for error in build_errors["errors"]:
            print("-------------------------")
            print(error)
            print("-------------------------")
        print("=============================")
        exit(1)

def sign():
    """
    Signs the manifest
    """
    sp.check_call(["{}/gluon/contrib/sign.sh".format(ARGS.workspace), ARGS.secret,
                   "{}/output/images/sysupgrade/{}.manifest".format(ARGS.workspace,
                                                                    DEFAULTS['branch'])])

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
            sp.check_call(["mkdir", "-p", dir_target])
            sp.check_call(["rsync", "-Ltr", "--remove-source-files", dir_source, dir_target])

        dir_source = "{}/output/images/".format(ARGS.workspace)
        dir_target = "{}/{}".format(directory, DEFAULTS['branch'])
        sp.check_call(["rsync", "-Ltr", dir_source, dir_target])

        print("delete images in workdir...")
        sp.check_call(["rm", "-rf", dir_source])
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

    if ARGS.cores is not None:
        print("INFO: Cores = {}".format(ARGS.cores))
        DEFAULTS['make_cores'] = ARGS.cores

    if ARGS.log is not None:
        print("INFO: Log = {}".format(ARGS.log))
        DEFAULTS['make_loglevel'] = ARGS.log

    if "/" in ARGS.branch:
        DEFAULTS['branch'] = ARGS.branch.split("/")[1]
        print("Warning: found \"/\" in branch name, changing to: {}".format(DEFAULTS['branch']))

    if ARGS.command == "clean":
        clean()
    elif ARGS.command == "dirclean":
        dirclean()
    elif ARGS.command == "update":
        update()
    elif ARGS.command == "build":
        build()
    elif ARGS.command == "sign":
        sign()
    elif ARGS.command == "publish":
        publish()
    else:
        raise ValueError("Command can only be one of: clean |"+
                         " dirclean | update | build | sign | publish")


if __name__ == '__main__':
    main()
