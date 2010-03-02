base = "http://www.heyzap.com"

counters = {
    "Front Page" :
        [("uri", base)],
    "Payments Page" :
        [("uri", base+"payments")],
    "Payments Item Lookup" :
        [("uri", base+"payments/get_item")],
    "Game Plays with Weebly embed key" :
        [("controller", "heyzap"),
         ("action", "index"),
         ("permalink", lambda s: s!=None)],
    }

def update_counts(counts, entry):
    for counter_name in counters:
        for key,test in counters[counter_name]:
            value = entry[key]
            if hasattr(test,"__call__"):
                passed = test(value)
            else:
                passed = value == test
            if not passed:
                break
        if passed:
            counts[counter_name] += 1
    return counts
