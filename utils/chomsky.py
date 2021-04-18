import re
import itertools

left, right = 0, 1


def list_union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list


def load_file(model_path):
    file = open(model_path).read()
    K, V, P = (file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", "")), \
              (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n", "").replace("\n", "")), \
              (file.split("Productions:\n")[1])

    return process_alphabet_input(K), process_alphabet_input(V), process_production_input(P)


def process_production_input(expression):
    result = []
    raw_rules = expression.replace('\n', '').split(';')

    for rule in raw_rules:
        left_side_terms = rule.split(' -> ')[0].replace(' ', '')
        right_side_terms = rule.split(' -> ')[1].split(' | ')
        for term in right_side_terms:
            result.append((left_side_terms, term.split(' ')))
    return result


def process_alphabet_input(expression):
    return expression.replace('  ', ' ').split(' ')


def check_primary_conditions(target, productions):
    trash, erased = [], []
    for production in productions:
        if target in production[right] and len(production[right]) == 1:
            trash.append(production[left])
        else:
            erased.append(production)

    return trash, erased


def get_input_dictionary(productions, variables, terms):
    result = {}
    for production in productions:
        #
        if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
            result[production[right][0]] = production[left]
    return result


def rewrite(target, production):
    result = []
    # get positions corresponding to the occurrences of target in production right side
    positions = [i for i, x in enumerate(production[right]) if x == target]
    # for all found targets in production
    for i in range(len(positions) + 1):
        # for all combinations of all possible length phrases of targets
        for element in list(itertools.combinations(positions, i)):
            # Example: if positions is [1 4 6]
            # now i've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
            # erase position corresponding to the target in production right side
            right_side_updated = [production[right][i] for i in range(len(production[right])) if i not in element]
            if right_side_updated:
                result.append((production[left], right_side_updated))
    return result


def dictionary_to_set_convert(dictionary):
    result = []
    for key in dictionary:
        result.append((dictionary[key], key))
    return result


def print_rules(rules):
    for rule in rules:
        tot = ""
        for term in rule[right]:
            tot = tot + " " + term
        print(rule[left] + " -> " + tot)


def prettify(rules):
    dictionary = {}
    for rule in rules:
        if rule[left] in dictionary:
            dictionary[rule[left]] += ' | ' + ' '.join(rule[right])
        else:
            dictionary[rule[left]] = ' '.join(rule[right])
    result = ""
    for key in dictionary:
        result += key + " -> " + dictionary[key] + "\n"
    return result
