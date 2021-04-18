# Made by: Cambur Dumitru
# Group: FAF-191
# Variant: (32 + 1) - 7 = 26

import sys
from utils import chomsky

left, right = 0, 1

K, V, Productions = [], [], []
variable_container = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                      "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W",
                      "X", "Y", "Z"]


def is_unitary(rule, variables):
    if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
        return True
    return False


def is_simple(rule):
    if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
        return True
    return False


for non_terminal in V:
    if non_terminal in variable_container:
        variable_container.remove(non_terminal)


# Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def first_step(productions, variables):
    variables.append('S0')
    return [('S0', [variables[0]])] + productions


# Remove rules containing both terms and variables, like A->Bc, replacing by A->BZ and Z->c–––––––––––TERM
def remove_term(productions, variables):
    new_productions = []
    # create a dictionary for all base production, like A->a, in the form dic['a'] = 'A'
    dictionary = chomsky.get_input_dictionary(productions, variables, terms=K)
    for production in productions:
        # check if the production is simple
        if is_simple(production):
            # in that case there is nothing to change
            new_productions.append(production)
        else:
            for term in K:
                for index, value in enumerate(production[right]):
                    if term == value and not term in dictionary:
                        # it's created a new production variable->term and added to it
                        dictionary[term] = variables.pop()
                        V.append(dictionary[term])
                        new_productions.append((dictionary[term], [term]))

                        production[right][index] = dictionary[term]
                    elif term == value:
                        production[right][index] = dictionary[term]
            new_productions.append((production[left], production[right]))

    # merge created set and the introduced rules
    return new_productions


# Eliminate non unitary rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def eliminate_non_unitary(productions, variables):
    result = []
    for production in productions:
        k = len(production[right])
        if k <= 2:
            result.append(production)
        else:
            new_var = variables.pop(0)
            variables.append(new_var + '1')
            result.append((production[left], [production[right][0]] + [new_var + '1']))
            i = 1
            for i in range(1, k - 2):
                var, var2 = new_var + str(i), new_var + str(i + 1)
                variables.append(var2)
                result.append((var, [production[right][i], var2]))
            result.append((new_var + str(k - 2), production[right][k - 2:k]))
    return result


# Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def delete_non_terminal_rules(productions):
    new_set = []
    outlaws, productions = chomsky.check_primary_conditions(target='e', productions=productions)
    for outlaw in outlaws:
        # consider every production: old + new resulting important when more than one outlaws are in the same prod.
        for production in productions + [e for e in new_set if e not in productions]:
            # if outlaw is present in the right side of a rule
            if outlaw in production[right]:
                # the rule is rewritten in all combination of it, rewriting "e" rather than outlaw
                # this cycle prevent to insert duplicate rules
                new_set = new_set + [e for e in chomsky.rewrite(outlaw, production) if e not in new_set]

    # add unchanged rules and return
    return new_set + ([productions[i] for i in range(len(productions))
                       if productions[i] not in new_set])


def unit_routine(rules, variables):
    unitary, result = [], []
    for rule in rules:
        if is_unitary(rule, variables):
            unitary.append((rule[left], rule[right][0]))
        else:
            result.append(rule)
    for uni in unitary:
        for rule in rules:
            if uni[right] == rule[left] and uni[left] != rule[left]:
                result.append((uni[left], rule[right]))

    return result


def unit(productions, variables):
    i = 0
    result = unit_routine(productions, variables)
    tmp = unit_routine(result, variables)
    while result != tmp and i < 1000:
        result = unit_routine(tmp, variables)
        tmp = unit_routine(result, variables)
        i += 1
    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_path = str(sys.argv[1])
    else:
        input_path = 'example'

    K, V, Productions = chomsky.load_file(input_path)

    Productions = first_step(Productions, variables=V)
    Productions = remove_term(Productions, variables=V)
    Productions = eliminate_non_unitary(Productions, variables=V)
    Productions = delete_non_terminal_rules(Productions)
    Productions = unit(Productions, variables=V)

    print(chomsky.prettify(Productions))
    open('out.txt', 'w').write(chomsky.prettify(Productions))
