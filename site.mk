# Enable the multidomain feature enables ffsh, ffrz and ffod.
GLUON_MULTIDOMAIN=1

# Just a placeholder, will be overwritten by the build script.
DEFAULT_GLUON_RELEASE := 1.1.1-$(shell date '+%Y%m%d')
GLUON_RELEASE ?= $(DEFAULT_GLUON_RELEASE)

# Default priority for the updater, overwritten by build script.
GLUON_PRIORITY ?= 0

# Default language and region.
GLUON_LANGS ?= en de
GLUON_REGION ?= eu

# What to do with deprecated devices, we still provide upgrades but no factory images.
GLUON_DEPRECATED ?= upgrade