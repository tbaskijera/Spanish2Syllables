import re

VOWELS = ["a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú", "ü"]
STRONG_VOWELS = ["a", "á", "e", "é", "o", "ó", "í", "ú", "ü"]
WEAK_VOWELS = ["i", "u"]
CONSONANTS = ["x", "j", "t", "s", "c", "g", "l",
              "f", "ll", "m", "r", "rr", "p", "h", "y", "ñ", "b", "d", "k", "n", "q", "v", "z", "ch", "w"]
UNALLOWED = ["pr", "pl", "br", "bl", "fr", "fl", "gr", "gl", "cr", "cl", "dr", "tr", "tl"]
STRONG_STRONG_VOWEL_PAIRS = ["ae", "ao", "ea", "eo", "oa", "oe", "óa"] # dali treba dodati parove sa naglascima
WEAK_WEAK_VOWEL_PAIRS = ["iu", "ui"]
STRONG_WEAK_VOWEL_PAIRS = ["ai", "ei", "oi", "au", "eu", "ou", "ia", "ie" "io", "ua", "ue", "uo"] # dali treba dodati parove sa naglascima
WEAK_STRONG_WEAK_VOWEL_TRIFTONG = ["iai", "iái","iau", "iáu", "iei", "iéi", "ieu", "iéu", "ioi", "iói", "iou", "ióu",
                                   "uai", "uái", "uau", "uáu", "uei", "uéi", "ueu", "uéu", "uoi", "uói", "uou", "uóu"]                   
INSEPARABLE = ["ns", "bs", "rs", "ps", "gs", "cs", "ks", "ds", "ts", "ms", "ls", "vs", "fs"]
STRONG_WEAK_TO_STRONG_VOWEL_PAIRS = ["aí", "aú", "aü", "eí", "eú", "eü", "oí", "oú", "oü",
                                    "ía", "úa", "üa", "íe", "úe", "üe", "ío", "úo", "üo"]

test_list = ["casa", "oprimo", "obrero",  "aflojar", "cafre", "hablando", "agrandar", "aglutinar", 
            "acróbata", "aclamar", "cuadro", "cuatro", "atlas", "atlalilco", "inseparable", "artista",
            "comedlo", "ponedla", "empleados", "englobar", "constitución", "instaurar", "obstinado",
            "instalar", "perspectiva", "aéreo", "pelear", "leo", "aire", "europa", "ásia", "cuidado",
            "ruidoso", "triunfante", "bioinformática", "radioisótopo", "asociáis", "buey", "había", "país", "reúno"]


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


def deformalize(string1, string2):
    list_of_char = []
    br = 0
    for i in string1:
        if i == "-":
            list_of_char.append(" ")
        else:
            list_of_char.append(string2[br])
            br += 1
    deformalized_string = ''.join(list_of_char)
    return deformalized_string


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


def rule_3(formalism, string):
    pattern = re.finditer("VCCCV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        consonant1 = pattern_start+1
        consonant2 = pattern_start+2
        consonant3 = pattern_start+3
        offset = check_offset(formalism, pattern_start)
        end_two = string[consonant2 - offset] + string[consonant3 - offset]
        first_two = string[consonant1 - offset] + string[consonant2 - offset]
        if end_two in UNALLOWED:
            formalism = re.sub('VCCCV', 'VC-CCV', formalism, 1)
        elif first_two in INSEPARABLE:
            formalism = re.sub('VCCCV', "VCC-CV", formalism, 1)
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
        else:
            formalism = re.sub("VV", "VV", formalism, 1)
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
        vowel3 = pattern_start+2
        offset = check_offset(formalism, pattern_start)
        v_triftong = string[vowel1-offset] + string[vowel2-offset] + string[vowel3-offset]
        if v_triftong in WEAK_STRONG_WEAK_VOWEL_TRIFTONG:
            formalism = re.sub("VVV", "VVV", formalism, 1)
    return formalism


def rule_8(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in STRONG_WEAK_TO_STRONG_VOWEL_PAIRS:
            formalism = re.sub("VV", "V-V", formalism, 1)
    return formalism


def additional_rule_2(formalism, string):
    pattern = re.finditer("VCC", formalism)
    if pattern is None:
            return formalism
    for object in pattern:
        pattern_start = object.start()
        consonant1 = pattern_start+1
        consonant2 = pattern_start+2
        offset = check_offset(formalism, pattern_start)
        c_pair = string[consonant1 - offset] + string[consonant2 - offset]
        if c_pair in UNALLOWED:
            formalism = re.sub("VCC", "V-CC", formalism, 1)
        else:
            formalism = re.sub("VCC", "VC-C", formalism, 1)
    return formalism


def process(string):
    formalism = formalize(string)
    formalism = rule_1(formalism)
    formalism = rule_1(formalism)
    #formalism = rule_2(formalism, string)
    formalism1 = rule_2(formalism, string)
    formalism1 = rule_2(formalism1, string)
    formalism = rule_1(formalism1)
    formalism = rule_3(formalism, string)
    formalism = rule_4(formalism, string)
    formalism = rule_4(formalism, string)
    formalism = rule_5(formalism, string)
    formalism = rule_6(formalism, string)
    formalism = rule_7(formalism, string)
    formalism = rule_8(formalism, string)
    if len(formalism)>3 or len(formalism1)>3:
        if formalism[-4:] == "VCC\"" or formalism1[-4] == "VCC\"" or formalism[-3:] == "VCC" or formalism1[-3] == "VCC":
            formalism = additional_rule_2(formalism1, string)
            formalism = additional_rule_2(formalism, string)
    formalism = rule_4(formalism, string)
    formalism = rule_4(formalism, string)
    #print(formalism)
    deformalism = deformalize(formalism, string)
    # return formalism
    return deformalism
