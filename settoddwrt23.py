#!/usr/bin/python
import os, sys
sys.path.append('/var/service/qrwifi/libexec')
from set_to_ddwrt import *

def generate(wl_interface, ssid, key, authmode):
    nas_allow_authmode = {
        'WPA2-PSK' : 128,
        'WPA-PSK'  : 2,
    }
    if authmode not in nas_allow_authmode:
        raise Exception("disallowed auth mode %s" % authmode)
    nas_opt_authmode = nas_allow_authmode[authmode]

    setcmds = [
        '/usr/bin/head /tmp/nas.{wl_interface}lan.pid | /usr/bin/xargs kill',
        '/usr/sbin/wl ssid {ssid}',
        '(/usr/sbin/nas -P /tmp/nas.{wl_interface}lan.pid -H 34954 -l br0 -i eth1 -A -m {auth} -k {key} -s {ssid} -w 4 -g 3600 </dev/null >/dev/null 2>&1 &)',
        '/usr/sbin/nvram set {wl_interface}_wpa_psk="{key}"',
        '/usr/sbin/nvram set {wl_interface}_ssid="{ssid}"',
        '/usr/sbin/nvram set wl_wpa_psk="{key}"',
        '/usr/sbin/nvram set wl_ssid="{ssid}"',
        '/usr/sbin/nvram commit',
    ]

    cmdline = ' && '.join(setcmds).format(ssid=ssid,key=key,auth=nas_opt_authmode,wl_interface=wl_interface)
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
