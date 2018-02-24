#!/bin/bash -e
# ======================================================================
# Build script for Freifunk Suedholstein firmware runningn on Jenkins CI
#
# Source: https://github.com/ffsh
# Web: https://freifunk-suedholstein.de
#
# Credits:
#   - Freifunk Fulda:        Freifunk Darmstadt for your great support.
#   - Freifunk Suedholstein: Freifunk Fulda for this nice script!
# ======================================================================

# Default make options
MAKEOPTS="V=s -j 8"

# Default to build all Gluon targets if parameter -t is not set
TARGETS="ar71xx-generic ar71xx-tiny ar71xx-nand ar71xx-mikrotik mpc85xx-generic x86-generic x86-64"

# Default is set to use current work directory
SITEDIR="$(pwd)"

# Default build identifier set to snapshot
BUILD="testing"

# Specify deployment server and user
DEPLOYMENT_SERVER="firmware.freifunk-suedholstein.de"
DEPLOYMENT_USER="deployment"

# Path to signing key
SIGNKEY=""

# Error codes
E_ILLEGAL_ARGS=126

# Help function used in error messages and -h option
usage() {
  echo ""
  echo "Build script for Freifunk-Suedholstein gluon firmware."
  echo ""
  echo "-b: Firmware branch name (e.g. development)"
  echo "    Default: current git branch"
  echo "-c: Build command: update | clean | download | build | sign | upload | prepare"
  echo "-d: Enable bash debug output"
  echo "-h: Show this help"
  echo "-m: Setting for make options (optional)"
  echo "    Default: \"${MAKEOPTS}\""
  echo "-n: Build identifier (optional)"
  echo "    Default: \"${BUILD}\""
  echo "-t: Gluon targets architectures to build"
  echo "    Default: \"${TARGETS}\""
  echo "-r: Release number (optional)"
  echo "    Default: fetched from release file"
  echo "-w: Path to site directory"
  echo "    Default: current working directory"
  echo "-s: Path to signing key"
  echo "    Default: empty"
}

# Evaluate arguments for build script.
if [[ "${#}" == 0 ]]; then
  usage
  exit ${E_ILLEGAL_ARGS}
fi

# Evaluate arguments for build script.
while getopts b:c:dhm:n:t:w:s: flag; do
  case ${flag} in
    b)
        BRANCH="${OPTARG}"
        ;;
    c)
      case "${OPTARG}" in
        update)
          COMMAND="${OPTARG}"
          ;;
        clean)
          COMMAND="${OPTARG}"
          ;;
        download)
          COMMAND="${OPTARG}"
          ;;
        build)
          COMMAND="${OPTARG}"
          ;;
        sign)
          COMMAND="${OPTARG}"
          ;;
        upload)
          COMMAND="${OPTARG}"
          ;;
        prepare)
          COMMAND="${OPTARG}"
          ;;
        *)
          echo "Error: Invalid build command set."
          usage
          exit ${E_ILLEGAL_ARGS}
          ;;
      esac
      ;;
    d)
      set -x
      ;;
    h)
      usage
      exit
      ;;
    m)
      MAKEOPTS="${OPTARG}"
      ;;
    n)
      BUILD="${OPTARG}"
      ;;
    t)
      TARGETS="${OPTARG}"
      ;;
    r)
      RELEASE="${OPTARG}"
      ;;
    w)
      # Use the root project as site-config for make commands below
      SITEDIR="${OPTARG}"
      ;;
    s)
      SIGNKEY="${OPTARG}"
      ;;
    *)
      usage
      exit ${E_ILLEGAL_ARGS}
      ;;
  esac
done

# Strip of all remaining arguments
shift $((OPTIND - 1));

# Check if there are remaining arguments
if [[ "${#}" > 0 ]]; then
  echo "Error: To many arguments: ${*}"
  usage
  exit ${E_ILLEGAL_ARGS}
fi

# Set branch name
if [[ -z "${BRANCH}" ]]; then
  BRANCH=$(git symbolic-ref -q HEAD)
  BRANCH=${BRANCH##refs/heads/}
  BRANCH=${BRANCH:-HEAD}
fi

# Set command
if [[ -z "${COMMAND}" ]]; then
  echo "Error: Build command missing."
  usage
  exit ${E_ILLEGAL_ARGS}
fi

# Set release number
if [[ -z "${RELEASE}" ]]; then
  RELEASE=$(cat "${SITEDIR}/release")
fi

# Normalize the branch name
BRANCH="${BRANCH#origin/}" # Use the current git branch as autoupdate branch
BRANCH="${BRANCH//\//-}"   # Replace all slashes with dashes

# Get the GIT commit description
COMMIT="$(git describe --always --dirty)"

# Number of days that may pass between releasing an updating
PRIORITY=1

update() {
  make ${MAKEOPTS} \
       GLUON_SITEDIR="${SITEDIR}" \
       GLUON_OUTPUTDIR="${SITEDIR}/output" \
       GLUON_RELEASE="${RELEASE}-${BUILD}" \
       GLUON_BRANCH="${BRANCH}" \
       GLUON_PRIORITY="${PRIORITY}" \
       update
}

clean() {
  for TARGET in ${TARGETS}; do
    echo "--- Update Gluon Dependencies for target: ${TARGET}"
    make ${MAKEOPTS} \
         GLUON_SITEDIR="${SITEDIR}" \
         GLUON_OUTPUTDIR="${SITEDIR}/output" \
         GLUON_RELEASE="${RELEASE}-${BUILD}" \
         GLUON_BRANCH="${BRANCH}" \
         GLUON_PRIORITY="${PRIORITY}" \
         GLUON_TARGET="${TARGET}" \
         clean
  done
}

download() {
  for TARGET in ${TARGETS}; do
    echo "--- Download Gluon Dependencies for target: ${TARGET}"
    make ${MAKEOPTS} \
         GLUON_SITEDIR="${SITEDIR}" \
         GLUON_OUTPUTDIR="${SITEDIR}/output" \
         GLUON_RELEASE="${RELEASE}-${BUILD}" \
         GLUON_BRANCH="${BRANCH}" \
         GLUON_PRIORITY="${PRIORITY}" \
         GLUON_TARGET="${TARGET}" \
         download
  done
}

build() {
  for TARGET in ${TARGETS}; do
    echo "--- Build Gluon Images for target: ${TARGET}"
    case "${BRANCH}" in
      stable| \
      testing| \
      development)
        make ${MAKEOPTS} \
             GLUON_SITEDIR="${SITEDIR}" \
             GLUON_OUTPUTDIR="${SITEDIR}/output" \
             GLUON_RELEASE="${RELEASE}-${BUILD}" \
             GLUON_BRANCH="${BRANCH}" \
             GLUON_PRIORITY="${PRIORITY}" \
             GLUON_TARGET="${TARGET}" \
             all
        ;;

      *)
        make ${MAKEOPTS} \
             GLUON_SITEDIR="${SITEDIR}" \
             GLUON_OUTPUTDIR="${SITEDIR}/output" \
             GLUON_RELEASE="${RELEASE}-${BUILD}" \
             GLUON_BRANCH="${BRANCH}" \
             GLUON_TARGET="${TARGET}" \
             all
      ;;
    esac
  done

  echo "--- Build Gluon Manifest"
  make ${MAKEOPTS} \
       GLUON_SITEDIR="${SITEDIR}" \
       GLUON_OUTPUTDIR="${SITEDIR}/output" \
       GLUON_RELEASE="${RELEASE}-${BUILD}" \
       GLUON_BRANCH="${BRANCH}" \
       GLUON_PRIORITY="${PRIORITY}" \
       manifest

  echo "--- Write Build file"
  cat > "${SITEDIR}/output/images/build" <<EOF
DATE=$(date '+%Y-%m-%d %H:%M:%S')
VERSION=$(cat "${SITEDIR}/release")
RELEASE=${RELEASE}
BUILD=${BUILD}
BRANCH=${BRANCH}
COMMIT=${COMMIT}
HOST=$(uname -n)
EOF
}

sign() {
  echo "--- Sign Gluon Firmware Build"

  # Add the signature to the local manifest
  contrib/sign.sh \
      "${SIGNKEY}" \
      "${SITEDIR}/output/images/sysupgrade/${BRANCH}.manifest"
}

upload() {
  echo "--- Upload Gluon Firmware Images and Manifest"

  # Build the ssh command to use
  SSH="ssh"
  SSH="${SSH} -o stricthostkeychecking=no"
  SSH="${SSH} -p 22022"

  # Determine upload target prefix
  case "${BRANCH}" in
    stable| \
    testing| \
    development)
      TARGET="${BRANCH}"
      ;;

    *)
      TARGET="others/${BRANCH}"
      ;;
  esac

  # Create the target directory on server
  ${SSH} \
      ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER} \
      -- \
      mkdir \
          --parents \
          --verbose \
          "firmware/${TARGET}/${RELEASE}-${BUILD}"

  # Copy images to server
  rsync \
      --verbose \
      --recursive \
      --compress \
      --progress \
      --links \
      --rsh="${SSH}" \
      "${SITEDIR}/output/images/" \
      "${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER}:firmware/${TARGET}/${RELEASE}-${BUILD}"

  # Link latest upload in target to 'current'
  ${SSH} \
      ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER} \
      -- \
      ln \
          --symbolic \
          --force \
          --no-target-directory \
          "${RELEASE}-${BUILD}" \
          "firmware/${TARGET}/current"
}

prepare() {
  echo "--- Prepare directory for upload"

  # Determine upload target prefix
  case "${BRANCH}" in
    stable| \
    testing| \
    development)
      TARGET="${BRANCH}"
      ;;

    *)
      TARGET="others/${BRANCH}"
      ;;
  esac

  # Create the target directory on server
  mkdir \
    --parents \
    --verbose \
    "${SITEDIR}/output/firmware/${TARGET}"

  # Copy images to directory
  mv \
    --verbose \
    "${SITEDIR}/output/images" \
    "${SITEDIR}/output/firmware/${TARGET}/${RELEASE}-${BUILD}"

  # Link latest upload in target to 'current'
  cd "${SITEDIR}/output"
  ln \
      --symbolic \
      --force \
      --no-target-directory \
      "${RELEASE}-${BUILD}" \
      "firmware/${TARGET}/current"
}

(
  # Change working directory to gluon tree
  cd "${SITEDIR}/gluon"

  # Execute the selected command
  ${COMMAND}
)
