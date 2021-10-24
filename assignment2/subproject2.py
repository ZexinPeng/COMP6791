pipeline_output_file = "./posting-list.txt"

if __name__ == '__main__':
    with open(pipeline_output_file, "r") as f:
        dic = eval(f.read())
        while True:
            term = input()
            posting_list = dic.get(term)
            if posting_list is None:
                print("no such term.")
                continue
            print("posting list length: " + str(len(posting_list)))
            print(posting_list)
