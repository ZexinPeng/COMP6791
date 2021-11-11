pipeline_output_file = "./posting-list.txt"
punctuations = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''


def get_term_lsit(query):
    term_list = []
    for term in query.split(" "):
        for character in term:
            if character in punctuations:
                token_list = list(term)
                token_list.pop(term.index(character))
                term = "".join(token_list)
        term_list.append(term)
    return term_list


def get_intersection(listA, listB):
    if len(listB) == 0:
        return listA
    if listA is None:
        return listB
    return list(set(listA).intersection(set(listB)))


if __name__ == '__main__':
    with open(pipeline_output_file, "r") as f:
        dic = eval(f.read())
        while True:
            print("please input the query term: ")
            query = input()
            term_list = get_term_lsit(query)
            res = []
            print(dic["Grootvlei"])
            for term in term_list:
                res = get_intersection(dic.get(term), res)
            print(res)