def doc_to_text(line):
    return """
    ## Question: {question}

    ## Choices:
    A. {option1}
    B. {option2}
    C. {option3}
    D. {option4}
    """.format(
        question=line["question"],
        option1=line["choices"][0],
        option2=line["choices"][1],
        option3=line["choices"][2],
        option4=line["choices"][3],
    ).strip()


def doc_to_target(line) -> int:
    return line["answer"]

def doc_to_choice(line):
    return ["A", "B", "C", "D"]