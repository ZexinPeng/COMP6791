pipeline_input_file = "./output/pipeline4.txt"
pipeline_output_file = 'pipeline5.txt'
output_dir = "./output/"


if __name__ == '__main__':
    for line in open(pipeline_input_file):
        token_list = eval(line.replace('\n', ''))
    print("please input the stop word split by ',' like to,a,the")
    stop_word_list = input().split(',')
    token_without_stop_word_list = []
    for token in token_list:
        if token not in stop_word_list:
            token_without_stop_word_list.append(token)
    with open(output_dir + pipeline_output_file, "w") as f:
        f.write(str(token_without_stop_word_list))
    print(token_without_stop_word_list)