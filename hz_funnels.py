import re


def gen_regex_test(p):
    def regex_test(c):
        matches = re.findall(p,element)
        return len(matches) > 0:
    return regex_test


base = "http://www.heyzap.com"

funnel_paths = [
{"name": "Publishers front page",
 "test": base,
 "next":[{"name":"new_site",
          "test":base+"/publishers/new_site",
          "next":[{"name":"get_embed",
                   "test":gen_regex_test(base+"/publishers/get_embed/\w*$"),
                   "next":[]
                   }]
          }]
 },
{"name": "Developer front page",
 "test": base,
 "next":[{"name":"developers",
          "test":base+"/developers",
          "next":[{"name":"new_game",
                   "test":base+"/developers/new_game",
                   "next":[]
                   },
                  {"name":"import_games",
                   "test":base+"/developers/import_games",
                   "next":[]
                   },
                  {"name":"upload_game_simple",
                   "test":base+"/developers/upload_game_simple",
                   "next":[]
                   }]
          }]
 }
]
 
class Funnel(object):
    def __init__(self, funnel_path):
        self.count = 0
        self.name = funnel_path["name"]
        self.hits = set()
        
        test = funnel_path["test"]
        if hasattr(test,"__call__"):
            self.test = test
        else:
            self.test = lambda s: test == s["uri"]
            
        self.children = [Funnel(path) for path in funnel_path["next"]]

    def pour(self, entry):
        if self.test(history):
            if self.hits.add(entry["ip"]):
                self.count += 1
        if entry["ip"] in self.hits:
          for child in self.children:
              child.pour(entry)


funnels = [Funnel(path) for path in funnel_paths]
