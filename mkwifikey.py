#!/usr/bin/python
import os,sys
import json
import random
import string
import tempfile

DATA_DIR = "./"

_default_authmode = 'WPA2-PSK'
_allow_authmode = ('WPA2-PSK',)

def id_generator(size=31, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def main():
    argv = sys.argv
    argc = len(argv)

    if(argc < 2):
        print("%s (labels...)" % (argv[0]))
        sys.exit(255)

    data = dict()
    datadir = DATA_DIR
    tmpfile = tempfile.mkstemp(suffix='', prefix='tmp', dir=datadir)
    file = "%s/%s" % (datadir, "keys.json")

    for label in (argv[1:]):
        ssid = id_generator(size=31, chars=string.ascii_uppercase + string.digits)
        keys = id_generator(size=63, chars=string.hexdigits)

        authmode = _default_authmode
        if '=' in label:
            (label,authmode) = label.split('=')
        if authmode not in _allow_authmode:
            raise Exception("disallow auth mode %s" % authmode)

        data[label] = [ ssid, keys, authmode ]

    with os.fdopen(tmpfile[0], 'w') as f:
        json.dump(data, f)
        f.flush()
        os.fsync(f.fileno())
        f.close()

    os.chmod(tmpfile[1], 0644)
    os.rename(tmpfile[1], file)

    sys.exit()

main()
