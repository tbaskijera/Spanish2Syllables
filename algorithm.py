import re

VOWELS = ["a", "e", "i", "o", "u"]
STRONG_VOWELS = ["a", "e", "o"]
WEAK_VOWELS = ["i", "u"]
CONSONANTS = ["á", "é", "í", "ó", "ú", "ü", "x", "j", "t", "s", "c", "g", "l",  # ["á", "é", "í", "ó", "ú", "ü"] samoglasnici ili ne?
              "f", "ll", "m", "r", "rr", "p", "h", "y", "ñ", "b", "d", "k", "n", "q", "v", "z", "ch", "w"]
UNALLOWED = ["pr", "pl", "br", "bl", "fr",
             "fl", "gr", "gl", "cr", "cl", "dr", "tr"]


def is_vowel(char):
    return char == 'V'


def is_consonant(char):
    return char == 'C'


def formalize(string):
    formalized_string = ""
    for letter in string:
        if letter in VOWELS:
            formalized_string += "V"
        elif letter in CONSONANTS:
            formalized_string += "C"
        else:
            pass  # ???
    return formalized_string


"""
def rule_1(formalism):
    formatted = ""
    for count, letter in enumerate(formalism):
        if is_consonant(letter) and count not in [0, 1]:
            if (is_vowel(formalism[count-1]) and is_vowel(formalism[count+1])):
                formatted += '-' + letter
        else:
            formatted += letter
    return formatted
"""


def rule_1(formalism):
    return re.sub('VCV', 'V-CV', formalism)


def rule_2(formalism, string):
    pattern = re.search("VCCV", formalism)
    if pattern is not None:
        pattern_start = pattern.start()
        consonant1 = pattern_start+1
        consonant2 = pattern_start+2
        c_pair = string[consonant1] + string[consonant2]
        if c_pair in UNALLOWED:
            return re.sub('VCCV', 'V-CCV', formalism)
        else:
            return re.sub('VCCV', "VC-CV", formalism)
    else:
        return formalism


def process(string):
    formalism = formalize(string)
    formalism = rule_1(formalism)
    formalism = rule_2(formalism, string)
    print(formalism)


process("casa")  # radi
process("oprimo")  # radi
