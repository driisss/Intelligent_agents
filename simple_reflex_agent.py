A = (0,0)
B = (0,1)

rules = {
    (A, "Dirty") : "Clean",
    (A, "Clean") : "Right",
    (B, "Dirty") : "Clean",
    (B, "Clean") : "Left",
}
def interpret_input(percept):
    # later can be real input/complex perception
    return percept

def rule_match(state, rules):
    return rules.get(state)

def simple_reflex_agent(percept):
    state = interpret_input(percept)
    action = rule_match(state, rules)
    return action

def run():
    print( simple_reflex_agent((A, "Dirty")),  )
    print( simple_reflex_agent((A, "Clean")),  )
    print( simple_reflex_agent((B, "Dirty")),  )
    print( simple_reflex_agent((B, "Clean")),  )

run()

