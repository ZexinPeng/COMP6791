import re
from nltk.corpus import stopwords
from tabulate import tabulate
from nltk import PorterStemmer

pipeline_output_file = "./posting-list.txt"
num2 = 0


def remove_numbers(info, dic):
    num = 0
    for key in dic.keys():
        num += len(dic.get(key))
    info.get('number for nonpositional postings').append(num)

    keys_need_removed = []
    for key in dic.keys():
        if re.search("[0-9]", key) is not None:
            keys_need_removed.append(key)
    for key in keys_need_removed:
        dic.pop(key)
    global num2
    term_list = info.get('number for terms')
    term_list.append(len(dic))
    info.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))
    info.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))


def nonpositional_postings_statistic_line1(info, dic):
    num = 0
    for key in dic.keys():
        num += len(dic.get(key))
    term_list = info.get('number for nonpositional postings')
    term_list.append(num)
    info.get('Δ % ').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))
    info.get('T % ').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))


def nonpositional_postings_statistic_line2(info, dic, index):
    num = 0
    for key in dic.keys():
        num += len(dic.get(key))
    term_list = info.get('number for nonpositional postings')
    term_list.append(num)
    info.get('Δ % ').append('{:0.2f}'.format(-100 * (term_list[index] - term_list[index + 1]) / term_list[index]))
    info.get('T % ').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[index + 1]) / term_list[0]))


def case_folding(info, dic):
    new_dict = {}
    for key in dic:
        if new_dict.get(key.lower()) is None:
            new_dict[key.lower()] = dic.get(key)
        else:
            new_dict[key.lower()] = merge_list_in_order(dic.get(key), new_dict[key.lower()])
    term_list = info.get('number for terms')
    term_list.append(len(new_dict))
    info.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[1] - term_list[2]) / term_list[1]))
    info.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[2]) / term_list[0]))
    return new_dict


def merge_list_in_order(upper_list, lower_list):
    tmp = []
    i = 0
    j = 0
    while i < len(upper_list) and j < len(lower_list):
        if int(upper_list[i]) < int(lower_list[j]):
            tmp.append(upper_list[i])
            i += 1
        elif int(upper_list[i]) > int(lower_list[j]):
            tmp.append(lower_list[j])
            j += 1
        else:
            tmp.append(upper_list[i])
            i += 1
            j += 1
    while j < len(lower_list):
        tmp.append(lower_list[j])
        j += 1
    while i < len(upper_list):
        tmp.append(upper_list[i])
        i += 1
    return tmp


def stopwords_removal(info, dic, num, index):
    stopwords_list = stopwords.words('english')[0: num - 1]
    new_dic = {}
    for key in dic.keys():
        if key not in stopwords_list:
            new_dic[key] = dic.get(key)
    term_list = info.get('number for terms')
    term_list.append(len(new_dic))
    info.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[2] - term_list[index]) / term_list[2]))
    info.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[index]) / term_list[0]))
    return new_dic


def porter_stemmer(info, dic, index):
    new_dict = {}
    for key in dic.keys():
        word_after_stem = PorterStemmer().stem(key)
        if new_dict.get(word_after_stem) is None:
            new_dict[word_after_stem] = dic.get(key)
        else:
            new_dict[word_after_stem] = merge_list_in_order(new_dict[word_after_stem], dic.get(key))
    term_list = info.get('number for terms')
    term_list.append(len(new_dict))
    info.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[index - 1] - term_list[index]) / term_list[index - 1]))
    info.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[index]) / term_list[0]))
    return new_dict


if __name__ == '__main__':
    dic = {}
    with open(pipeline_output_file, "r") as f:
        dic = eval(f.read())

    info = {' ': ['unfiltered', 'no numbers', 'case folding', '30 stop words', '150 stop words', 'stemming'],
            'number for terms': [len(dic)],
            'Δ %': [' '],
            'T %': [' '],
            'number for nonpositional postings': [],
            'Δ % ': [' '],
            'T % ': [' ']
            }

    # remove all numbers
    remove_numbers(info, dic)
    nonpositional_postings_statistic_line1(info, dic)

    # case folding
    dic = case_folding(info, dic)
    nonpositional_postings_statistic_line2(info, dic, 1)

    # 30 stop words removal
    stopwords30_dic = stopwords_removal(info, dic, 30, 3)
    nonpositional_postings_statistic_line2(info, stopwords30_dic, 2)

    # 150 stop words removal
    dic = stopwords_removal(info, dic, 150, 4)
    nonpositional_postings_statistic_line2(info, dic, 3)

    # porter stemmer
    dic = porter_stemmer(info, dic, 5)
    nonpositional_postings_statistic_line2(info, dic, 4)

    print(tabulate(info, headers='keys'))

    while True:
        term = input()
        posting_list = dic.get(PorterStemmer().stem(term))
        if posting_list is None:
            print("no such term.")
            continue
        print("term after stemmed: " + PorterStemmer().stem(term) + ", posting list length: " + str(len(posting_list)))
        print(posting_list)


