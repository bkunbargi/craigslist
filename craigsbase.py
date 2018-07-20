from pathlib import Path



def file_parse(path_):
    path = Path(path_)
    for filename in path.iterdir():
        for file in filename.iterdir():
            reading_file = open(file,'r')
            for line in reading_file.readlines():
                print(line)

file_parse('output')
