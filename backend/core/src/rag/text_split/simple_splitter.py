class SimpleSplitter:
    def __init__(self, num_tokens=1000, overlap=200, split_tokens=['。', '\n']):
        self.num_tokens = num_tokens
        self.overlap = overlap
        self.split_tokens = split_tokens

    def split(self, text):
        texts = self._split_by_tokens(text)
        texts = self._filter_blank(texts)

    def _split_by_tokens(self, text):
        text = text.replace('\r', '')
        texts = [text]
        for s in self.split_tokens:
            new_splits = []
            for t in texts:
                new_splits.extend(t.split(s))
            texts = new_splits

    def _filter_blank(self, texts):
        strip = [t.strip() for t in texts]
        return [t for t in strip if t]

    def _merge_to_chunk(self, texts):
        chunks = []
        chunk_start = 0
        while True:
            chunk = ''
            for i in range(chunk_start, len(texts)):
                if len(chunk) + len(texts[i]) < self.num_tokens:
                    chunk += texts[i]
                else:
                    break
            chunks.append(chunk)
            if i == len(texts) - 1:
                break

            n_overlap = 0
            for chunk_start in range(0, chunk_start, -1):
                n_overlap += len(texts[chunk_start])
                if n_overlap >= self.overlap:
                    break

        return chunks
