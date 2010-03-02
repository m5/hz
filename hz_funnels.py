import re


def gen_regex_test(p):
    def regex_test(c):
        for element in c:
            if type(element) == type(""):
                matches = re.findall(p,element)
                if len(matches) > 0:
                    return True
        return False
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
        
        test = funnel_path["test"]
        if hasattr(test,"__call__"):
            self.test = test
        else:
            self.test = lambda s: test in s
            
        self.children = [Funnel(path) for path in funnel_path["next"]]

    def pour(self, history):
        if self.test(history):
            self.count += 1
            for child in self.children:
                child.pour(history)


funnels = [Funnel(path) for path in funnel_paths]
