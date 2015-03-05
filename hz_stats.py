#! /usr/bin/env python

from collections import defaultdict
from hz_parser import get_entries
from hz_counters import update_counts, counters
from hz_funnels import funnels
from mako.template import Template
import datetime
import sys
import glob
import os

usage = """%s <log file path> <out file path>
Parses the most recent log file in `in file path`,
and outputs statistics under the current date in `out file path`""" % sys.argv[0]

def helpful_exit():
    print usage
    sys.exit(0)


def get_stats(f):
    counts = defaultdict(lambda:0)
    uniques = defaultdict(set)
    for entry in get_entries(f):
        counts = update_counts(counts, entry)
        if entry["ip"]:
            uniques[entry["ip"]].add(entry["uri"])
            for funnel in funnels:
                funnel.pour(entry)

    return counts, funnels, uniques

def write_stats(counts, funnels, today, path='./'):
    stats_temp = Template(filename="stats.mako")
    today_pretty = today.strftime("%A, %B %d, %Y")
    today_filename = today.strftime("%Y-%m-%d.html")
    html = stats_temp.render(counts=counts,
                             funnels=funnels,
                             today=today_pretty)
    f = open(os.path.join(path,today_filename),'w')
    f.write(html)
    f.close()
    

if __name__ == "__main__":
    try:
        in_path = sys.argv[1]
    except IndexError:
        print usage
        sys.exit(1)
        
    try:
        out_path = sys.argv[2]
    except IndexError:
        print usage
        sys.exit(1)

    dir_contents = glob.glob(in_path+'/*')
    try:
        filename = sorted(dir_contents,key=lambda f: os.path.getctime(f))[0]
    except IndexError:
        print usage
        sys.exit
        
    f = open(filename)
    counts, funnels, uniques = get_stats(f)
    write_stats(counts, funnels, datetime.date.today(), out_path)


