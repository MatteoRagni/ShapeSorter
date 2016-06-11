#!/usr/bin/env python

import itertools as it
#from math import floor
import pickle
from time import sleep
import socket
import json

from glob import glob
from os import stat


frequency = 60
target_sim = ("localhost", 9999)
config = {
    "elements": 3,
    "rows": 5,
    "cols": 5,
    "el_name": ("l3", "l4", "lr"),
    "translate": -2,
    "scale": 1.2
}

###########################################################


def ntocs(n, config):
    cs = config["cols"]
    r = n // cs
    c = n - r * cs
    return [r, c]


def rcreal(a, config):
    b = [0, 0]
    b[0] = round((a[0] + config["translate"]) * config["scale"], 2)
    b[1] = round((a[1] + config["translate"]) * config["scale"], 2)
    return b


def cston(r, c, config):
    return (r * config["cols"]) + c


def allpos(config):
    return range(config["rows"] * config["cols"])


def create_list(config):
    return list(
        it.permutations(
            allpos(config),
            config["elements"]
        )
    )


def print_list(lst, config):
    head = "Iter\t" + (("%s\t" * config["elements"]) % config["el_name"])
    print(head)
    for i, l in enumerate(lst):
        line = "%i\t" % i
        for a, b in enumerate(l):
            c = ntocs(b, config)
            line += "(%3d,%3d)\t" % (c[0], c[1])
        print(line)


def write_file(name, lst, config):
    print("Writing %d position elements in %s file..." % (len(lst), name))
    new_lst = []
    new_lst2 = []
    new_lst3 = []
    for i, l in enumerate(lst):
        obj = {}
        obj2 = {}
        obj3 = {}
        for a, b in enumerate(l):
            obj[a] = rcreal(ntocs(b, config), config)
            obj2[a] = ntocs(b, config)
            obj3[a] = b
        new_lst.append(obj)
        new_lst2.append(obj2)
        new_lst3.append(obj3)
    config["data"] = new_lst
    config["perms"] = new_lst2
    config["pos"] = new_lst3
    ff = open(name, 'wb')
    pickle.dump(config, ff)
    ff.close()

###########################################################


def send_request(sock, name, x, y):
    data = {
        "com": "moveit",
        "val": {"name": name, "x": x, "y": y}
    }
    s_data = json.dumps(data)
    sock.sendto(bytes(s_data, "utf-8"), target_sim)


def execute_screen(sock, name):
    data = {
        "com": "screenshot",
        "val": "dataset/" + name
    }
    s_data = json.dumps(data)
    sock.sendto(bytes(s_data, "utf-8"), target_sim)


def iterate(sock, config):
    for idx, d in enumerate(config["data"]):
        print("Executing %d of %d (%3.2f%%)" % (idx, len(config["data"]), 100 * idx / len(config["data"])))
        for k in d:
            v = d[k]
            name = config["el_name"][k]
            send_request(sock, name, v[0], v[1])
            sleep(1 / frequency)
        execute_screen(sock, "dataset/take_%06d.png" % (idx))


###########################################################

lst = create_list(config)
write_file("perm_25_3.pkl", lst, config)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
iterate(sock, config)

##########################################################


def clean_null_png():
    files = glob("*.png")
    # null_idx = []
    for f in files:
        st = stat(f)
        if st.st_size == 0:
            print(f)
