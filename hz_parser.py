from __future__ import generators
from collections import defaultdict
import re

def get_entries(f):
    entry = defaultdict(lambda:None)
    for line in f:
        if line == "\n" and entry != {}:
            yield entry
            entry = defaultdict(lambda:None)
        else:
            try:
                line_type = line.strip().split()[0]
                new_params = parsers[line_type](line)
                entry.update(new_params)
            except IndexError:
                continue
            except KeyError:
                continue

            
def parse_processing(line):
    words = line.split()
    try:
        ip = words[3]
    except IndexError:
        ip = None
        
    try:
        controller, action = words[2].split('#')
    except IndexError:
        controller = None
        action = None
    except ValueError:
        controller = None
        action = None
    
    return {"ip":ip, "controller":controller, "action":action}

   
def parse_parameters(line):
    params = re.findall(r'\"(.*?)\"=>\"(.*?)\"',line)
    return dict(params)

def parse_completed(line):
    try:
        uri = re.findall(r'\[(.*)\?',line)[0]
        uri = uri.strip('/')
    except IndexError:
        uri = None
    return {"uri":uri}
    

parsers = {
    "Processing" : parse_processing,
    "Parameters:" : parse_parameters,
    "Completed"  : parse_completed,
    }
