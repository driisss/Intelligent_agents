A = (0,0)
B = (0,1)

def reflex_agent(percept):
    location, status = percept
    if status == 'Dirty':
        return 'Clean'
    elif location == A:
        return 'Right'
    elif location == B:
        return 'Left'   
    
def run ():
    print (reflex_agent((A,'Dirty')),  ) # Clean
    print (reflex_agent((A,'Clean')),  ) # Right   
    print (reflex_agent((B,'Dirty')),  ) # Clean

run ()
