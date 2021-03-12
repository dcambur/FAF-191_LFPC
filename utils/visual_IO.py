"""
Module to manage IO
"""

import json
import graphviz
import os


def dfa_json_importer(input_file: str) -> dict:
    """ Imports a DFA from a JSON file."""
    file = open(input_file)
    json_file = json.load(file)

    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]
    for (origin, action, destination) in json_file['transitions']:
        transitions[origin, action] = destination

    dfa = {
        'alphabet': set(json_file['alphabet']),
        'states': set(json_file['states']),
        'initial_state': json_file['initial_state'],
        'accepting_states': set(json_file['accepting_states']),
        'transitions': transitions
    }
    return dfa


def dfa_to_json(dfa: dict, name: str, path: str = './'):
    """
    Exports a DFA to a JSON file.
    If *path* do not exists, it will be created.
    """
    out = {
        'alphabet': list(dfa['alphabet']),
        'states': list(dfa['states']),
        'initial_state': dfa['initial_state'],
        'accepting_states': list(dfa['accepting_states']),
        'transitions': list()
    }

    for t in dfa['transitions']:
        out['transitions'].append(
            [t[0], t[1], dfa['transitions'][t]])

    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(path, name + '.json'), 'w')
    json.dump(out, file, sort_keys=True, indent=4)
    file.close()


def dfa_to_dot(dfa: dict, name: str, path: str = './'):
    """ Generates a DOT file and a relative SVG image in **path**
    folder of the input DFA using graphviz library.
    """
    g = graphviz.Digraph(format='svg')
    g.node('fake', style='invisible')
    for state in dfa['states']:
        if state == dfa['initial_state']:
            if state in dfa['accepting_states']:
                g.node(str(state), root='true',
                       shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in dfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    g.edge('fake', str(dfa['initial_state']), style='bold')
    for transition in dfa['transitions']:
        g.edge(str(transition[0]),
               str(dfa['transitions'][transition]),
               label=transition[1])

    if not os.path.exists(path):
        os.makedirs(path)

    g.render(filename=os.path.join(path, name + '.dot'))


def nfa_json_importer(input_file: str) -> dict:
    """ Imports a NFA from a JSON file.
    """
    file = open(input_file)
    json_file = json.load(file)

    transitions = {}  # key [state in states, action in alphabet]
    #                   value [Set of arriving states in states]
    for p in json_file['transitions']:
        transitions.setdefault((p[0], p[1]), set()).add(p[2])

    nfa = {
        'alphabet': set(json_file['alphabet']),
        'states': set(json_file['states']),
        'initial_states': set(json_file['initial_states']),
        'accepting_states': set(json_file['accepting_states']),
        'transitions': transitions
    }

    return nfa


def nfa_to_json(nfa: dict, name: str, path: str = './'):
    """ Exports a NFA to a JSON file."""
    transitions = list()  # key[state in states, action in alphabet]
    #                       value [Set of arriving states in states]
    for p in nfa['transitions']:
        for dest in nfa['transitions'][p]:
            transitions.append([p[0], p[1], dest])

    out = {
        'alphabet': list(nfa['alphabet']),
        'states': list(nfa['states']),
        'initial_states': list(nfa['initial_states']),
        'accepting_states': list(nfa['accepting_states']),
        'transitions': transitions
    }

    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(path, name + '.json'), 'w')
    json.dump(out, file, sort_keys=True, indent=4)
    file.close()


def nfa_to_dot(nfa: dict, name: str, path: str = './'):
    """ Generates a DOT file and a relative SVG image in **path**
    folder of the input NFA using graphviz library.
    """
    g = graphviz.Digraph(format='svg')

    fakes = []
    for i in range(len(nfa['initial_states'])):
        fakes.append('fake' + str(i))
        g.node('fake' + str(i), style='invisible')

    for state in nfa['states']:
        if state in nfa['initial_states']:
            if state in nfa['accepting_states']:
                g.node(str(state), root='true',
                       shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in nfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    for initial_state in nfa['initial_states']:
        g.edge(fakes.pop(), str(initial_state), style='bold')
    for transition in nfa['transitions']:
        for destination in nfa['transitions'][transition]:
            g.edge(str(transition[0]), str(destination),
                   label=transition[1])

    g.render(filename=os.path.join(path, name + '.dot'))
