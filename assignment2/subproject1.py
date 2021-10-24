from nltk import word_tokenize
import os
import re

pipeline_output_file = "./posting-list.txt"
path = '../reuters21578'
punctuations = '''=\'+!()-[]{};:",<>./`?@#$%^&*_~'''
dictionary = {}


def read_from_file():
    for file in os.listdir(path):
        # find all files ending with .sgm in the folder
        if file.endswith('.sgm'):
            # use latin-1 to decode some characters excluded in utf-8 or gbk
            with open(os.path.join(path, file), 'r', encoding='latin-1') as f:
                reuters_file_content = f.read()
                yield reuters_file_content


def remove_duplicate(F):
    new_list = []
    for index in range(len(F) - 1):
        if F[index][0] != F[index + 1][0] or F[index][1] != F[index + 1][1]:
            new_list.append([F[index][0], F[index][1]])
    new_list.append([F[index][0], F[index][1]])
    return new_list


def construct_posting_list():
    for pair in F:
        posting_list = dictionary.get(pair[0])
        if posting_list is None:
            dictionary[pair[0]] = []
        dictionary.get(pair[0]).append(pair[1])


def store_in_disk():
    with open(pipeline_output_file, "w") as f:
        f.write(str(dictionary))


if __name__ == '__main__':
    F = []
    files = read_from_file()
    # iterate all .sgm files
    counts = 0
    for file in files:
        # get single document
        for document in re.findall("<REUTERS TOPICS.*?</REUTERS>", file.replace('\n', ' ')):
            document = document.replace("&lt", "")
            title_group = re.search("<TITLE>.*?</TITLE>", document)
            if title_group is None:
                continue
            title = title_group.group()[7: -8]
            body_group = re.search("<BODY>.*?</BODY>", document)
            if body_group is None:
                continue
            body = body_group.group()[6: -7]
            docID = re.search('''NEWID="[0-9]+"''', document).group()[7:-1]
            tokens = word_tokenize(title + " " + body)
            for token in tokens:
                if token == "''":
                    continue
                if len(token) == 1 and token in punctuations:
                    continue
                for character in token:
                    if character in punctuations:
                        token.replace(character, '')
                F.append([token, docID])

    F = sorted(F, key=(lambda x: [x[0]]))
    print("sort completed!")

    F = remove_duplicate(F)
    print("removal completed!")

    construct_posting_list()

    store_in_disk()








