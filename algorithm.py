import re

VOWELS = ["a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú", "ü"]
STRONG_VOWELS = ["a", "á", "e", "é", "o", "ó", "í", "ú", "ü"]
WEAK_VOWELS = ["i", "u"]
CONSONANTS = ["x", "j", "t", "s", "c", "g", "l",
              "f", "ll", "m", "r", "rr", "p", "h", "y", "ñ", "b", "d", "k", "n", "q", "v", "z", "ch", "w"]
UNALLOWED = ["pr", "pl", "br", "bl", "fr",
             "fl", "gr", "gl", "cr", "cl", "dr", "tr"]
STRONG_STRONG_VOWEL_PAIRS = ["ae", "ao", "ea", "eo", "oa", "oe"] # dodati parove sa naglascima
WEAK_WEAK_VOWEL_PAIRS = ["iu", "ui"] # dodati parove sa naglascima
STRONG_WEAK_VOWEL_PAIRS = ["ai", "ei", "oi", "au",
                           "eu", "ou", "ia", "ie" "io", "ua", "ue", "uo"] # dodati parove sa naglascima
WEAK_STRONG_WEAK_VOWEL_TRIFTONG = ["iai", "iái","iau", "iáu", "iei", "iéi", "ieu", "iéu", "ioi", "iói", "iou", "ióu",
                                   "uai", "uái", "uau", "uáu", "uei", "uéi", "ueu", "uéu", "uoi", "uói", "uou", "uóu"]                          


def is_vowel(char):
    return char == 'V'


def is_consonant(char):
    return char == 'C'


def check_offset(string, point):
    count = 0
    for i in range(point):
        if string[i] == "-":
            count += 1
    return count


def formalize(string):
    formalized_string = ""
    for letter in string:
        if letter in VOWELS:
            formalized_string += "V"
        elif letter in CONSONANTS:
            formalized_string += "C"
        else:
            formalized_string += letter
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
    pattern = re.finditer("VCCV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        consonant1 = pattern_start+1
        consonant2 = pattern_start+2
        offset = check_offset(formalism, pattern_start)
        c_pair = string[consonant1 - offset] + string[consonant2 - offset]
        if c_pair in UNALLOWED:
            formalism = re.sub('VCCV', 'V-CCV', formalism, 1)
        else:
            formalism = re.sub('VCCV', "VC-CV", formalism, 1)
    return formalism


def rule_4(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in STRONG_STRONG_VOWEL_PAIRS:
            formalism = re.sub("VV", "V-V", formalism, 1)
    return formalism


def rule_5(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in STRONG_WEAK_VOWEL_PAIRS:
            formalism = re.sub("VV", "VV", formalism, 1)
    return formalism


def rule_6(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in WEAK_WEAK_VOWEL_PAIRS:
            formalism = re.sub("VV", "VV", formalism, 1)
    return formalism


def rule_7(formalism, string):
    pattern = re.finditer("VVV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in WEAK_STRONG_WEAK_VOWEL_TRIFTONG:
            formalism = re.sub("VVV", "VVV", formalism, 1)
    return formalism


# rule_8 je odraden


def process(string):
# VAZNO VAZNO!! u rule bilo koji pronade prvi pattern npr VV i rastavi ga na V-V,
# ali ako se pojavi jos jednom u istoj rijeci onda ga ne nade
    formalism = formalize(string)
    formalism = rule_1(formalism)
    #formalism = rule_2(formalism, string)
    formalism1 = rule_2(formalism, string) # ovo popravlja problem sa agrandar isto i sa europa
    formalism1 = rule_2(formalism1, string)
    formalism = rule_1(formalism1) 
    formalism = rule_4(formalism, string)
    formalism = rule_4(formalism, string) # rjesava problem aereo
    formalism = rule_5(formalism, string)
    formalism = rule_6(formalism, string)
    formalism = rule_7(formalism, string)
    print(formalism)


process("oprimo")
process("pelear")

process("agrandar")
process("aéreo")
process("europa")
process("empleados")
