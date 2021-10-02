pipeline_input_file = "./output/pipeline2.txt"
pipeline_output_file = 'pipeline3.txt'
output_dir = "./output/"


if __name__ == '__main__':
    for line in open(pipeline_input_file):
        token_list = eval(line.replace('\n', ''))
    smallcase_token_list = []
    for token in token_list:
        smallcase_token_list.append(str.lower(token))
    with open(output_dir + pipeline_output_file, "w") as f:
        f.write(str(smallcase_token_list))
    print(smallcase_token_list)