GLUON_SITE_PACKAGES := \
    gluon-mesh-batman-adv-15 \
    gluon-respondd \
    gluon-autoupdater \
    gluon-config-mode-core \
    gluon-config-mode-hostname \
    gluon-config-mode-autoupdater \
    gluon-config-mode-mesh-vpn \
    gluon-config-mode-geo-location \
    gluon-config-mode-contact-info \
    gluon-ebtables-filter-multicast \
    gluon-ebtables-filter-ra-dhcp \
    gluon-web-admin \
    gluon-web-network \
    gluon-web-autoupdater \
    gluon-web-private-wifi \
    gluon-web-wifi-config \
    gluon-mesh-vpn-fastd \
    gluon-web-mesh-vpn-fastd \
    gluon-radvd \
    gluon-radvd-filterd \
    gluon-setup-mode \
    gluon-status-page \
    iwinfo \
    haveged \

# add offline ssid only if the target has wifi device
ifeq ($(GLUON_TARGET),ar71xx-generic)
GLUON_SITE_PACKAGES += \
    gluon-ssid-changer
endif

ifeq ($(GLUON_TARGET),ar71xx-tiny)
GLUON_SITE_PACKAGES += \
    gluon-ssid-changer
endif

ifeq ($(GLUON_TARGET),ar71xx-mikrotik)
GLUON_SITE_PACKAGES += \
    gluon-ssid-changer
endif

ifeq ($(GLUON_TARGET),ar71xx-nand)
GLUON_SITE_PACKAGES += \
    gluon-ssid-changer
endif

ifeq ($(GLUON_TARGET),mpc85xx-generic)
GLUON_SITE_PACKAGES += \
    gluon-ssid-changer
endif

ifeq ($(GLUON_TARGET),ramips-rt305x)
GLUON_SITE_PACKAGES += \
    gluon-ssid-changer
endif

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
        gluon-ssid-changer \
        kmod-usb-core \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

ifeq ($(GLUON_TARGET),brcm2708-bcm2709)
GLUON_SITE_PACKAGES += \
        gluon-ssid-changer \
        kmod-usb-core \
        kmod-usb2 \
        kmod-usb-hid \
        kmod-usb-net \
        kmod-usb-net-asix \
        kmod-usb-net-dm9601-ether
endif

ifeq ($(GLUON_TARGET),sunxi)
GLUON_SITE_PACKAGES += \
        gluon-ssid-changer \
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
GLUON_LANGS ?= en de
GLUON_REGION ?= eu
GLUON_ATH10K_MESH=11s
