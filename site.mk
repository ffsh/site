GLUON_FEATURES := \
    autoupdater \
    ebtables-filter-multicast \
    ebtables-filter-ra-dhcp \
    ebtables-limit-arp \
    mesh-batman-adv-15 \
    mesh-vpn-wireguard \
    radv-filterd \
    respondd \
    status-page \
    web-advanced \
    web-wizard \
    web-private-wifi \
    config-mode-domain-select

GLUON_SITE_PACKAGES := \
    iwinfo \

GLUON_SITE_PACKAGES_standard := \
    respondd-module-airtime \

GLUON_MULTIDOMAIN=1

DEFAULT_GLUON_RELEASE := 1.1.1-$(shell date '+%Y%m%d')
GLUON_RELEASE ?= $(DEFAULT_GLUON_RELEASE)

GLUON_PRIORITY ?= 0

GLUON_LANGS ?= en de
GLUON_REGION ?= eu

GLUON_DEPRECATED ?= upgrade

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

# Add network drivers and usb stuff to raspberry and banana pi images

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