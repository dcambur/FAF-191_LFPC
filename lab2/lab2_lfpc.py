# Made by: Cambur Dumitru
# Group: FAF-191
# Variant: (32 + 1) - 7 = 26
from utils import visual_IO, NFA

json_auto = visual_IO.nfa_json_importer("input.json")
dfa = NFA.convert_to_dfa(json_auto)
visual_IO.dfa_to_dot(dfa, "dfa")
