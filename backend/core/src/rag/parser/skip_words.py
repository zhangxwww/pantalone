import os


SKIP_WORDS = set()

with open(os.path.join(os.path.dirname(__file__), 'skip.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            SKIP_WORDS.add(line)
