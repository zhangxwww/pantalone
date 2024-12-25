from itertools import zip_longest


def batcher(iterable, batch_size):
    args = [iter(iterable)] * batch_size
    for batch in zip_longest(*args):
        yield [i for i in batch if i is not None]
