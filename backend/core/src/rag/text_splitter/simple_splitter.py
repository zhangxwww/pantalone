class SimpleSplitter:
    def __init__(self, max_tokens=1000, max_overlap=200, split_tokens=['。', '?', '？', '!', '！', '\n']):
        self.max_tokens = max_tokens
        self.max_overlap = max_overlap
        self.split_tokens = split_tokens

    def split(self, text):
        texts = self._split_by_tokens(text)
        texts = self._filter_blank(texts)
        chunks = self._merge_to_chunk(texts)
        return chunks

    def _split_by_tokens(self, text):
        text = text.replace('\r', '')
        texts = [text]
        for s in self.split_tokens:
            new_splits = []
            for t in texts:
                new_splits.extend(t.split(s))
            texts = new_splits
        return texts

    def _filter_blank(self, texts):
        strip = [t.strip() for t in texts if t]
        return [t for t in strip if t]

    def _merge_to_chunk(self, texts):
        if not texts:
            return []
        text_lengths = {text: len(text) for text in texts}
        text_num = len(texts)
        chunks = []

        k = 0
        while k < text_num:
            chunk_length = text_lengths[texts[k]]

            if chunk_length > self.max_tokens:
                chunks.append(texts[k][:self.max_tokens])
                k += 1
                continue

            i = k
            overlap_length = 0
            while i > 0:
                if overlap_length + text_lengths[texts[i - 1]] > self.max_overlap or chunk_length + overlap_length + text_lengths[texts[i - 1]] > self.max_tokens:
                    break
                overlap_length += text_lengths[texts[i - 1]]
                i -= 1

            j = k
            new_chunk_length = chunk_length
            while j < text_num - 1:
                if new_chunk_length + text_lengths[texts[j + 1]] > self.max_tokens - overlap_length:
                    break
                new_chunk_length += text_lengths[texts[j + 1]]
                j += 1

            chunks.append(''.join(texts[i : j+1]))
            k = j + 1

        return chunks
