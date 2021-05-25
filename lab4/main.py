# Made by: Cambur Dumitru
# Group: FAF-191
# Variant: 7

# Global Variables Declaration

V_N = ['S', 'A', 'B', 'C']
V_T = ['a', 'b', 'd']
P = ["S->aA", "A->C", "C->CbA", "C->dB", "B->b", "B->aB"]

WORD = "adbbdb"

STATES = {}
FIRST = {}
LAST = {}
PRECEDENCE_MATRIX = {}
ALL_SYMBOLS = V_N + V_T
ALL_SYMBOLS.append('$')


def read_input():
    for el in P:
        symbols = []
        if el[0] not in STATES.keys():
            STATES[el[0]] = []

        for symbol in el:
            if symbol != '-' and symbol != '>':
                symbols.append(symbol)
        STATES[symbols.pop(0)].append(symbols)


def first_last():
    def add_first_last(left_side, recurrent_left_side, pos, dictionary):
        for rightSide in STATES[recurrent_left_side]:
            if rightSide[pos] not in dictionary[left_side]:
                dictionary[left_side].append(rightSide[pos])
                if rightSide[pos] in V_N:
                    add_first_last(left_side, rightSide[pos], pos, dictionary)

    for nonTerminal in V_N:
        FIRST[nonTerminal] = []
        LAST[nonTerminal] = []
        add_first_last(nonTerminal, nonTerminal, 0, FIRST)
        add_first_last(nonTerminal, nonTerminal, -1, LAST)


def complete_matrix(dictionary):
    def init_matrix(array):
        for el in array:
            PRECEDENCE_MATRIX[el] = {}
            for element in array:
                PRECEDENCE_MATRIX[el][element] = []
                if el == '$' and element != '$':
                    PRECEDENCE_MATRIX['$'][element] = ['<']
            if el != '$':
                PRECEDENCE_MATRIX[el]['$'] = ['>']

    def execute_rules():

        def rule1():
            PRECEDENCE_MATRIX[production[count]][production[count + 1]].append('=')

        def rule2():
            if production[count + 1] in V_N:
                for symbol in FIRST[production[count + 1]]:
                    PRECEDENCE_MATRIX[production[count]][symbol].append('<')

        def rule3():
            if production[count] in V_N and production[count + 1] in V_T:
                for symbol in LAST[production[count]]:
                    PRECEDENCE_MATRIX[symbol][production[count + 1]].append('>')
            elif production[count] in V_N and production[count + 1] in V_N:
                for symbol in LAST[production[count]]:
                    for symbol2 in FIRST[production[count + 1]]:
                        if symbol2 in V_T:
                            PRECEDENCE_MATRIX[symbol][symbol2].append('>')

        rule1()
        rule2()
        rule3()

    init_matrix(ALL_SYMBOLS)
    for leftSide, rightSide in dictionary.items():
        for production in rightSide:
            if len(production) > 1:
                count = 0
                while count < len(production) - 1:
                    execute_rules()
                    count += 1


def print_matrix(matrix):
    def format_start():
        print("{:<5}".format(' '), end=' ')

    def upper_elements_print():
        for element in ALL_SYMBOLS:
            print("{:<5}".format(element), end=' ')

    def print_by_rows():
        for element, array_element in matrix.items():
            print("\n{:<5}".format(element), end=' ')
            for symbol in array_element:
                if len(array_element[symbol]) == 0:
                    print("{:<5}".format(' '), end=' ')
                else:
                    print("{:<5}".format(array_element[symbol][0]), end=' ')
        [print() for _ in range(2)]

    format_start()
    upper_elements_print()
    print_by_rows()


def verify_input(to_verify, matrix):
    def print_parse(array):
        for term in array:
            print(term, end="")
        print()

    def replace_term():
        for left_side, right_side in STATES.items():
            if symbols in right_side:
                return ["<", left_side, ">"]

    new_input = ["$"]
    i = 1
    while to_verify[i] != "$":
        if to_verify[i] == "<":
            i += 1
            start = i - 1
            symbols = []

            while to_verify[i] != ">":
                if to_verify[i] == "<":
                    for j in range(start, i):
                        new_input.append(to_verify[j])
                    symbols = []
                    i -= 1
                    break
                if to_verify[i] in ALL_SYMBOLS:
                    symbols.append(to_verify[i])
                i += 1
            i += 1
            if len(symbols) == 1:
                if to_verify[i] != '$':
                    if matrix[to_verify[i - 2]][to_verify[i]][0] == "=":
                        new_input.extend(["<", to_verify[i - 2], "="])
                    elif matrix[to_verify[i - 4]][to_verify[i - 2]][0] == "=":
                        new_input.extend(["=", to_verify[i - 4], ">"])
                    else:
                        new_input.extend(replace_term())
                else:
                    if matrix[to_verify[start - 1]][to_verify[start + 1]][0] == "=":
                        new_input.extend(["=", to_verify[start + 1], ">"])
                    else:
                        new_input.extend(replace_term())
            elif len(symbols) > 0:
                new_input.append("<")
                for left_side, right_side in STATES.items():
                    if symbols in right_side:
                        new_input.append(left_side)
                        new_input.append(">")
        else:
            new_input.append(to_verify[i])
            i += 1
    new_input.append("$")
    print_parse(new_input)
    if len(new_input) > 5:
        verify_input(new_input, matrix)


def parse_input(new_input, matrix):
    input_list = []
    for i in range(0, (len(new_input) - 1) * 2, 2):
        new_input = new_input[:i + 1] + matrix[new_input[i]][new_input[i + 1]][0] + new_input[i + 1:]
    for symbol in new_input:
        input_list.append(symbol)
    verify_input(input_list, matrix)


read_input()
first_last()
complete_matrix(STATES)
print_matrix(PRECEDENCE_MATRIX)
parse_input("$" + WORD + "$", PRECEDENCE_MATRIX)
