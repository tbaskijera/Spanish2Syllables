from algorithm import process
import docx2txt
import re

# prvo procitat liniju po liniju
# onda odvojit u dvije liste 
# jedna lista primjer, druga lista odvojeno
# na kraju usporedit process(primjer[1]) == odvojeno[1] 

def convert_docx2txt(file):
    content_docx = docx2txt.process(file)
    with open("output.txt", "w", encoding='utf-8') as text_file:
        print(content_docx, file=text_file)


def delete_blank_line(file):
    with open(file, 'r', encoding='utf-8') as reader, open(file, 'r+', encoding='utf-8') as writer:
        for line in reader:
            if line.strip():
                writer.write(line)
        writer.truncate()


def split_element_from_list():
    new_list = []
    f = open('output.txt', 'r', encoding='utf-8')
    for line in f:
        new_list.append(re.split('–|-', line))
    # join sublists - list
    new_list = sum(new_list, [])
    return new_list


def create_two_list(list):
    list_words_for_test = []
    list_syllables_compare = []
    list_syllables = []
    true_counter = 0
    # stvaranje lista - jedna za elemete za testiranje - druga sa elemetima za usporedbu
    for i in range(0, len(list)):
        if i % 2 == 0:
            list_words_for_test.append(list[i])
        else:
            list_syllables_compare.append(list[i])
    
    for item in list_words_for_test:
        add = process(item)
        list_syllables.append(add.replace(" ", "."))

    for i in range(0, len(list_syllables)):
        if list_syllables[i] == list_syllables_compare [i]:
            true_counter += 1
    
    # ove dvije liste treba urediti - ocistiti od nepotrebnih razmaka, \n, ., "", i sl.
    print(list_syllables)
    print(list_syllables_compare)
    return true_counter

def average(list):
    return create_two_list(list)/(len(list))  


convert_docx2txt('SPANISH_primjeri.docx')
delete_blank_line('output.txt')
split_list = split_element_from_list()

create_two_list(split_list)
print("Postotak točnosti je:", average(split_list))