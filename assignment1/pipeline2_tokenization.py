from nltk import word_tokenize
import os

pipeline_input_file = "pipeline1.txt"
pipeline_output_file = 'pipeline2.txt'
output_dir = "./output/"


if __name__ == '__main__':
    counts = 0
    actual_output_dir = output_dir + str(counts) + '/'
    while os.path.exists(actual_output_dir):
        for line in open(actual_output_dir + pipeline_input_file):
            text_dict = eval(line.replace('\n', ''))
            tokens = word_tokenize(text_dict['content'])
        special_symbols = '''!()-[]{};:'",<>./``''?@#$%^&*_~'''
        token_list = []
        # clean all special symbols in the tokens
        for token in tokens:
            if token not in special_symbols and token != '--':
                token_list.append(token)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(actual_output_dir + pipeline_output_file, "w") as f:
            f.write(str(token_list))
        actual_output_dir = output_dir + str(counts) + '/'
        counts += 1
