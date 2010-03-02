from collections import defaultdict
from hz_parser import get_entries
from hz_counters import update_counts, counters
from hz_funnels import funnels
from mako.template import Template
import datetime
import sys

def get_stats(f):
    counts = defaultdict(lambda:0)
    uniques = defaultdict(set)
    for entry in get_entries(f):
        counts = update_counts(counts, entry)
        if entry["ip"]:
            uniques[entry["ip"]].add(entry["uri"])

    for ip,history in uniques.iteritems():
        for funnel in funnels:
            funnel.pour(history)
            
    return counts, funnels, uniques

def write_stats(counts, funnels, today, path='./'):
    stats_temp = Template(filename="stats.mako")
    today_pretty = today.strftime("%A, %B %d, %Y")
    today_filename = today.strftime("%Y-%m-%d")+".html"
    html = stats_temp.render(counts=counts,
                             funnels=funnels,
                             today=today_pretty)
    f = open(path+today_filename,'w')
    f.write(html)
    f.close()
    

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "data/heyzap-example-log"

    try:
        path = sys.argv[2]
    except IndexError:
        path = "./"
    
    f = open(filename)
    counts, funnels, uniques = get_stats(f)
    write_stats(counts, funnels, datetime.date.today(), path)
