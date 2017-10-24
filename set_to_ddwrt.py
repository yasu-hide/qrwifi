#!/usr/bin/python
import os,sys
import subprocess
import json

DATA_DIR="/var/service/qrwifi/data"
KEY_JSON="%s/%s" % (DATA_DIR, "keys.json")
SSH_BIN="/usr/bin/ssh"
SSH_USR="root"
SSH_KEY="%s/%s" % (DATA_DIR, "id_dsa.nopass")

def load(label):
    data = dict()
    with open(KEY_JSON, "r") as f:
        data = json.load(f)
        f.close()

    if label not in data:
        print "LABEL %s not exists" % (label)
        sys.exit(1)
    (ssid, key, authmode) = data[label]
    return (ssid, key, authmode)

def set_to_ddwrt(routerip, cmdline):
    env = { 'DISPLAY' : ':9999' }
    cmd = [SSH_BIN,'-T', '-l',SSH_USR,'-i',SSH_KEY,routerip, cmdline]

    p = subprocess.Popen(cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        preexec_fn=os.setsid,
    )

    (stdout,stderr, stdin) = (p.stdout, p.stderr, p.stdin)
    if stderr:
        while True:
            line = stderr.readline()
            if not line:
                break
            print line.rstrip()

    if stdout:
        while True:
            line = stdout.readline()
            if not line:
                break
            print line.rstrip()

    ret = p.wait()
    return ret
