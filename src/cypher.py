from . import des

import os

ALGORITHMS = {
    "des" : des
}

def _get_message_from_file(filename):
    absolute_filepath  = os.path.abspath(f"input/{filename}")
    with open(absolute_filepath) as file:
        lines = file.readlines()

    return " ".join(lines).replace("\n", "")

def apply_cypher(input_type, algorithm, operation, keywords, message="", filename=""):
    if input_type == "file":
        message = _get_message_from_file(filename)

    keywords = keywords.split()
    result = ALGORITHMS.get(algorithm).apply(text=message, key=keywords, mode=operation)

    return result