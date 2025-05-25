def process_docs(dataset):
    return dataset.filter(lambda line: len(line["choices"]) == 4)
