"""
Module to manage NFA (Nondeterministic Finite Automata).
In this module a NFA is defined as follows

 NFA = dict() with the following keys-values:

  • alphabet         => set() ;
  • states           => set() ;
  • initial_states   => set() ;
  • accepting_states => set() ;
  • transitions      => dict(), where
        **key**: (state in states, action in alphabet)

        **value**: {set of arriving states in states}.

"""


# NFA to DFA
def convert_to_dfa(nfa: dict) -> dict:
    """ Returns a DFA that reads the same language of the input NFA.
    :param dict nfa: input NFA.
    :return: *(dict)* representing a DFA
    """
    dfa = {
        'alphabet': nfa['alphabet'].copy(),
        'initial_state': None,
        'states': set(),
        'accepting_states': set(),
        'transitions': dict()
    }

    if len(nfa['initial_states']) > 0:
        dfa['initial_state'] = str(nfa['initial_states'])
        dfa['states'].add(str(nfa['initial_states']))

    sets_states = list()
    sets_queue = list()
    sets_queue.append(nfa['initial_states'])
    sets_states.append(nfa['initial_states'])
    if len(sets_states[0].intersection(nfa['accepting_states'])) > 0:
        dfa['accepting_states'].add(str(sets_states[0]))

    while sets_queue:
        current_set = sets_queue.pop(0)
        for a in dfa['alphabet']:
            next_set = set()
            for state in current_set:
                if (state, a) in nfa['transitions']:
                    for next_state in nfa['transitions'][state, a]:
                        next_set.add(next_state)
            if len(next_set) == 0:
                continue
            if next_set not in sets_states:
                sets_states.append(next_set)
                sets_queue.append(next_set)
                dfa['states'].add(str(next_set))
                if next_set.intersection(nfa['accepting_states']):
                    dfa['accepting_states'].add(str(next_set))

            dfa['transitions'][str(current_set), a] = str(next_set)

    return dfa

