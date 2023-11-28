def get_employers_from_txt(filename):
    """Возвращает список компаний из текстового файла"""

    employers_ = []
    with open(filename, 'rt') as file:
        for line in file:
            employers_.append(line.split(" - ")[0])
    return employers_
