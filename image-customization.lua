features({
    'autoupdater',
    'ebtables-filter-multicast',
    'ebtables-filter-ra-dhcp',
    'ebtables-limit-arp',
    'mesh-batman-adv-15',
    'mesh-vpn-fastd',
    'web-mesh-vpn-fastd',
    'mesh-vpn-fastd-l2tp',
    'radv-filterd',
    'respondd',
    'status-page',
    'web-advanced',
    'web-wizard',
    'web-private-wifi',
    'config-mode-domain-select'
})

if not device_class('tiny') then
    features({
        'web-cellular',
    })
    packages({
        'respondd-module-airtime'
    })
end

packages({'iwinfo'})