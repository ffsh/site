#!/usr/bin/python3
"""
Build script for Freifunk Suedholstein firmware runningn on Jenkins CI

Source: https://github.com/ffsh/site
Web: https://freifunk-suedholstein.de

"""
import argparse
import json
import os

from datetime import datetime
import subprocess as sp

DEFAULT = {
    'targets' : ['ar71xx-generic',
                 'ar71xx-tiny',
                 'ar71xx-nand',
                 'brcm2708-bcm2708',
                 'brcm2708-bcm2709',
                 'mpc85xx-generic',
                 'ramips-mt7621',
                 'x86-generic',
                 'x86-geode',
                 'x86-64',
                 'ramips-mt7620',
                 'ramips-rt305x'
                ]}

"""
DEFAULTS = {
    'targets' : ['ar71xx-generic',
                 'ar71xx-tiny',
                 'ar71xx-nand',
                 'brcm2708-bcm2708',
                 'brcm2708-bcm2709',
                 'mpc85xx-generic',
                 'ramips-mt7621',
                 'x86-generic',
                 'x86-geode',
                 'x86-64',
                 'ramips-mt7620',
                 'ramips-rt305x'
                ],
    'gluon_dir': '/gluon',
    'make_cores' : "1",
    'make_loglevel': 'V=s',
    'release': '2018.1',
    'priority': 1,
    'branch': 'dev'
}"""

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
                    required=True)
PARSER.add_argument("--silent", action='store_true',
                    help="build.py --silent",
                    required=False)


ARGS = PARSER.parse_args()


class Builder():
    """docstring for Builder"""

    # pylint: disable=too-many-instance-attributes
    # go home pylint i need the attributes

    def __init__(self, build_env, firmware_release, publish_dir="", dump_all=False):
        super().__init__()

        # build_env
        self.site_path = build_env["site_path"]
        self.gluon_path = self.site_path+"/gluon"
        self.cores = build_env["cores"]
        self.log_level = build_env["log_level"]

        if build_env["silent_mode"]:
            self.make_mode = sp.DEVNULL
        else:
            self.make_mode = sp.STDOUT

        # firmware_release
        self.release = firmware_release["release"]
        self.build_number = firmware_release["build_number"]
        self.targets = firmware_release["targets"]
        self.branch = firmware_release["branch"]
        self.commit = firmware_release["commit"]
        self.secret = firmware_release["secret"]

        self.publish_dir = publish_dir

        if dump_all:
            print(json.dumps(build_env, indent=2))
            print(self.gluon_path)
            print(json.dumps(firmware_release, indent=2))
            print(publish_dir)
    def clean(self):
        """
        Cleans the output Directory. Not necessary!
        """
        for target in self.targets:
            print("Cleaning target: {}".format(target))
            sp.check_call(["make", "-C", self.gluon_path,
                           "GLUON_SITEDIR="+self.site_path,
                           "GLUON_TARGET="+target,
                           "clean"])

    def dirclean(self):
        """
        Clean with dirclean
        """
        print("Starting dirclean ...")
        sp.check_call(["make", "-C", self.gluon_path,
                       "GLUON_SITEDIR="+self.site_path,
                       "dirclean"])
        print("dirclean done.")

    def update(self):
        """
        Updates the repository
        """
        print("Starting update ...")
        sp.check_call(["make", "-C", self.gluon_path,
                       "GLUON_SITEDIR="+self.site_path,
                       "update"])
        print("Update done.")


    def build(self):
        """
        Build images definded by -t or default targets
        """
        print("Info: Starting building ...")
        print("Info: delete OLD images in workdir...")
        dir_source = "{}/output/images/".format(self.site_path)
        sp.check_call(["rm", "-rf", dir_source])
        build_errors = {
            "number": 0,
            "errors": []
        }


        for target in self.targets:
            print("Info: Building target: {}".format(target))
            try:
                sp.check_call(["make", "-j", self.cores, "-C",
                               self.gluon_path,
                               self.log_level,
                               "GLUON_SITEDIR="+self.site_path,
                               "GLUON_RELEASE={}-{}-{}".format(self.release,
                                                               self.build_number,
                                                               self.branch),
                               "GLUON_BRANCH="+self.branch,
                               "GLUON_OUTPUTDIR={}/output".format(self.site_path),
                               "GLUON_TARGET="+target,
                               "all"],
                              stderr=self.make_mode)

            except sp.CalledProcessError as process_error:
                print(process_error)
                build_errors["errors"].append(process_error)
                build_errors["number"] += 1

        print("Info: Generating buid.json")
        time_stamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        data = {
            'build_date' : time_stamp,
            'release' : "{}-{}-{}".format(self.release, self.branch,
                                          self.build_number),
            'branch' : self.branch,
            'commit' : self.commit
        }
        with open("{}/output/images/build.json".format(self.site_path), "w") as file:
            json.dump(data, file)

        # Create manifest
        print("Createing Manifest ...")

        if not os.path.isdir("{}/tmp/origin/".format(self.site_path)):
            # Make sure that the tmp dir exists
            sp.check_call(["mkdir", "-p", "{}/tmp/origin/".format(self.site_path)])

        sp.check_call(["make", "-C", self.gluon_path,
                       "GLUON_SITEDIR="+ARGS.workspace,
                       "GLUON_RELEASE={}-{}-{}".format(self.release,
                                                       ARGS.build_number,
                                                       self.branch),
                       "GLUON_BRANCH="+self.branch,
                       "GLUON_OUTPUTDIR={}/output".format(ARGS.workspace),
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

    def sign(self):
        """
        Signs the manifest
        """
        sp.check_call(["{}/gluon/contrib/sign.sh".format(self.site_path), self.secret,
                       "{}/output/images/sysupgrade/{}.manifest".format(self.site_path, self.branch)])

    def publish(self):
        """
        Copy the images to a public directory
        """

        if os.path.isdir(self.publish_dir):
            # direcotry/BRANCH/build.json
            if os.path.isdir("{}/{}".format(self.publish_dir, self.branch)):

                print("Detected old builds move to archive")
                dir_source = "{}/{}".format(self.publish_dir, self.branch)

                with open(dir_source+"/build.json") as file:
                    old_build_date = json.load(file)["build_date"]
                dir_target = "{}/archive/{}-{}".format(self.publish_dir, self.branch, old_build_date)
                sp.check_call(["mkdir", "-p", dir_target])
                sp.check_call(["rsync", "-Ltr", "--remove-source-files", dir_source, dir_target])

            dir_source = "{}/output/images/".format(ARGS.workspace)
            dir_target = "{}/{}".format(self.publish_dir, self.branch)
            sp.check_call(["rsync", "-Ltr", dir_source, dir_target])

            print("delete images in workdir...")
            sp.check_call(["rm", "-rf", dir_source])
        else:
            raise ValueError("{} Path does not exist!".format(self.publish_dir))
        #clean()

def main():
    """
    Entry function
    """
    # Create build configuration
    build_env = {}
    build_env["site_path"] = ARGS.workspace
    build_env["cores"] = ARGS.cores
    build_env["log_level"] = ARGS.log

    build_env["silent_mode"] = ARGS.silent

    if ARGS.cores is not None:
        print("INFO: Cores = {}".format(ARGS.cores))
        build_env["cores"] = ARGS.cores

    if ARGS.log is not None:
        print("INFO: Log = {}".format(ARGS.log))
        build_env["log_level"] = ARGS.log



    # Create firmware configuration
    firmware_release = {}

    firmware_release["secret"] = ARGS.secret

    # parse release.json
    with open(build_env["site_path"] + '/release.json', 'r') as file:
        data = json.load(file)
        firmware_release["release"] = data['version']
        # currently not used
        # firmware_release["priority"] = data['priority']
    firmware_release["build_number"] = ARGS.build_number

    # check for single target build
    if ARGS.target is not None:
        print("INFO: Single target: {}".format(ARGS.target))
        firmware_release["targets"] = [ARGS.target]
    else:
        firmware_release["targets"] = DEFAULT["targets"]

    # FIX branch name
    if "/" in ARGS.branch:
        firmware_release["branch"] = ARGS.branch.split("/")[1]
        print("Warning: found \"/\" in branch name, changing to: {}".format(firmware_release["branch"]))
    elif ARGS.branch is not None:
        firmware_release["branch"] = ARGS.branch
        print("Info: branch switched to: {}".format(firmware_release["branch"]))

    firmware_release["commit"] = ARGS.commit

    # publish config

    if ARGS.directory is not None:
        publish_dir = ARGS.directory
    else:
        publish_dir = ""

    # configs done; start builder
    builder = Builder(build_env, firmware_release, publish_dir, dump_all=True)

    if ARGS.command == "clean":
        builder.clean()
    elif ARGS.command == "dirclean":
        builder.dirclean()
    elif ARGS.command == "update":
        builder.update()
    elif ARGS.command == "build":
        builder.build()
    elif ARGS.command == "sign":
        builder.sign()
    elif ARGS.command == "publish":
        builder.publish()
    else:
        raise ValueError("Command can only be one of: clean |"+
                         " dirclean | update | build | sign | publish")


if __name__ == '__main__':
    main()
