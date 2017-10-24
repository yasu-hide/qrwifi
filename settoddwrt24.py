#!/usr/bin/python
import os, sys
sys.path.append('/var/service/qrwifi/libexec')
from set_to_ddwrt import *

def generate(wl_interface, ssid, key, authmode):
    setcmds = [
        "/bin/sed -i -e 's/^ssid=.*/ssid={ssid}/;s/wpa_passphrase=.*/wpa_passphrase={key}/' /tmp/{wl_interface}_hostap.conf",
        "/usr/bin/head /var/run/{wl_interface}_hostapd.pid | /usr/bin/xargs kill -HUP",
        '/usr/sbin/nvram set {wl_interface}_wpa_psk="{key}"',
        '/usr/sbin/nvram set {wl_interface}_ssid="{ssid}"',
        '/usr/sbin/nvram commit',
    ]

    cmdline = ' && '.join(setcmds).format(ssid=ssid,key=key,wl_interface=wl_interface)
    return cmdline

def main():
    argv = sys.argv
    argc = len(argv)

    if(argc != 4):
        print "%s <ROUTER_IP> <ROUTER_IF> <LABEL>" % (argv[0])
        sys.exit(255)

    routerip = argv[1]
    routerif = argv[2]
    label    = argv[3]

    (ssid, key, authmode) = load(label)
    cmdline = generate(routerif, ssid, key, authmode)
    ret = set_to_ddwrt(routerip, cmdline)

    sys.exit(ret)

main()
