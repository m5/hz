base = "http://www.heyzap.com"

funnel_paths = [
    ("Publishers front page",
        [base,
           [base+"/publishers/new_site",
              [base+"/publishers/get_embed",
               ]
            ]
         ],
     ),
    ("Developer front page",
        [base,
           [base+"/developers",
              [base+"/developers/new_game",
               base+"/developers/import_games",
               base+"/developers/new_inventory_item",
               base+"/developers/upload_game_simple",
               ],
            ]
         ],
     ),
]


class Funnel(object):
    def __init__(self, funnel_path, name=None):
        self.count = 0
        
        if isinstance(funnel_path,list):
            self.uri = funnel_path[0]
        else:
            self.uri = funnel_path
    
        self.children = []
        if not name:
            name = self.uri
        self.name = name

        try:
            if isinstance(funnel_path,list):
              for next_step in funnel_path[1:]:
                  child = Funnel((next_step))
                  self.children.append(child)
        except IndexError:
            pass

    def pour(self, history):
        if self.uri in history:
            self.count += 1
            for child in self.children:
                child.pour(history)

funnels = [Funnel(path,name=name) for name,path in funnel_paths]
