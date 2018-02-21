GLUON_FEATURES := \
    autoupdater \
    ebtables-filter-multicast \
    ebtables-filter-ra-dhcp \
    mesh-batman-adv-15 \
    mesh-vpn-fastd \
    radvd \
    respondd \
    status-page \
    web-advanced \
    web-wizard

GLUON_SITE_PACKAGES := \
    gluon-web-private-wifi \
    iwinfo \
    haveged \
    gluon-config-mode-domain-select

GLUON_MULTIDOMAIN=1

# add addition network drivers and usb stuff only to targes where disk space does not matter.
ifeq ($(GLUON_TARGET),x86-generic)
GLUON_SITE_PACKAGES += \
        kmod-usb-core \
        kmod-usb-ohci-pci \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

ifeq ($(GLUON_TARGET),x86-64)
GLUON_SITE_PACKAGES += \
        kmod-usb-core \
        kmod-usb-ohci-pci \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

# Add offline ssid, network drivers and usb stuff to raspberry and banana pi images

ifeq ($(GLUON_TARGET),brcm2708-bcm2708)
GLUON_SITE_PACKAGES += \
        kmod-usb-core \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

ifeq ($(GLUON_TARGET),brcm2708-bcm2709)
GLUON_SITE_PACKAGES += \
        kmod-usb-core \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

ifeq ($(GLUON_TARGET),sunxi)
GLUON_SITE_PACKAGES += \
        kmod-usb-core \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

DEFAULT_GLUON_RELEASE := 2018.1

GLUON_RELEASE ?= $(DEFAULT_GLUON_RELEASE)

#GLUON_BRANCH ?= testing
#export GLUON_BRANCH

#GLUON_TARGET ?= ar71xx-generic
#export GLUON_TARGET

# Default priority for updates.
GLUON_PRIORITY ?= 0

# Languages to include
GLUON_LANGS ?= en de fr
GLUON_REGION ?= eu
GLUON_ATH10K_MESH=11s
