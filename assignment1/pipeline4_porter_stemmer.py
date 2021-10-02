from nltk import PorterStemmer

pipeline_input_file = "./output/pipeline3.txt"
pipeline_output_file = 'pipeline4.txt'
output_dir = "./output/"


if __name__ == '__main__':
    for line in open(pipeline_input_file):
        token_list = eval(line.replace('\n', ''))
    token_porter_stemmer_list = []
    for token in token_list:
        token_porter_stemmer_list.append(PorterStemmer().stem(token))
    with open(output_dir + pipeline_output_file, "w") as f:
        f.write(str(token_porter_stemmer_list))
    print(token_porter_stemmer_list)