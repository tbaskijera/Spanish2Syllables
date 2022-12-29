from matplotlib import pyplot as plt
from algorithm import process
from tabulate import tabulate
import docx2txt
import re

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
        new_list.append(re.split(' – | - ', line))
    # join sublists - list
    new_list = sum(new_list, [])
    return new_list


def clean_list(list):
    clean_list = []
    for el in list:
        new_list=[]
        for i in el:
            if (i.isalpha()) == True or i == "\"" or i ==".":
                new_list.append(i)
        clean_list.append(''.join(new_list))
    return clean_list


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
    list_syllables_compare = clean_list(list_syllables_compare)
    for item in list_words_for_test:
        add = process(item)
        list_syllables.append(add.replace(" ", "."))

    for i in range(0, len(list_syllables)):
        if list_syllables[i] == list_syllables_compare[i]:
            true_counter += 1
        else:
            print("Krivi je:", list_syllables[i], " --- ", list_syllables_compare[i])
    return true_counter, list_syllables_compare, list_syllables, list_words_for_test


def save_table(table):
    with open('table.txt', 'w', encoding='utf-8') as f:
        f.write(table)


def average_graph(lists):
    lista = create_two_list(lists)

    # Creating pie chart
    corectVSincorrect = ['correct', 'incorrect']
    data = [lista[0], (len(lista[1])-lista[0])]
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot()
    ax.pie(data, labels = corectVSincorrect, colors=['green', 'red'], shadow = "True", explode = [0.1, 0.0], autopct = '%.1f%%')
    ax.set_title("A graph of correctly separated words for the first test")
    plt.legend(title = "Legend", loc = "best")
    # show plot
    plt.show()

    # Create table in terminal
    newList=[]
    lista3 = lista[3]
    lista2 = lista[2]
    lista1 = lista[1]
    for i in range(0, len(lista3)):
        newList.append([lista3[i], lista2[i], lista1[i]])
    header = ["Word", "Word2Syllables", "Correct Word2Syllables"]
    table = tabulate(newList, headers=header, tablefmt="fancy_grid")
    print(table)
    save_table(table)

    return (lista[0]/(len(lista[1])))*100


convert_docx2txt('SPANISH_primjeri.docx')
delete_blank_line('output.txt')
split_list = split_element_from_list()
print("Postotak točnosti je:", round(average_graph(split_list), 4))
