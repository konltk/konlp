import numpy as np

# 전역 변수 지정...
UNK = "$UNK$"  # 미등록어
NUM = "$NUM$"  # 숫자
SYM = "$SYM$"  # 기호
ETC = "$ETC$"  # 그 외의 문자...

NONE = "O"
BOS = "$BOS$"  # 문장의 시작.
EOS = "$EOS$"  # 문장의 끝.


# special error message
class MyIOError(Exception):
    def __init__(self, filename):
        # custom error message
        message = """
ERROR: Unable to locate file {}.

FIX: Have you tried running python build_data.py first?
This will build vocab file from your train, test and dev sets and
trimm your word vectors.
""".format(filename)
        super(MyIOError, self).__init__(message)


class CoNLLDataset(object):
    """Class that iterates over CoNLL Dataset

    __iter__ method yields a tuple (words, tags)
        words: list of raw words
        tags: list of raw tags

    If processing_word and processing_tag are not None, optional preprocessing is appplied

    Example:
        ```python
        data = CoNLLDataset(filename)
        for sentence, tags in data:
            pass
        ```

    """

    def __init__(self,
                 filename,  # CoNLL 파일명
                 processing_word=None,  #
                 processing_tag=None,
                 processing_pos=None,
                 processing_lexicon=None,
                 max_iter=None):
        """
        Args:
            filename: path to the file
            processing_word: (optional) function that takes a word as input
            processing_tag: (optional) function that takes a tag as input
            max_iter: (optional) max number of sentences to yield

        """
        self.filename = filename
        self.processing_word = processing_word
        self.processing_tag = processing_tag
        self.processing_pos = processing_pos
        self.processing_lexicon = processing_lexicon
        self.max_iter = max_iter
        self.length = None

    def __iter__(self):
        niter = 0
        with open(self.filename, 'rt', encoding='utf8') as f:
            words, tags = [], []
            poses = []
            for line in f:
                line = line.strip()
                if len(line) == 0 or line.startswith("-DOCSTART-"):
                    if len(words) != 0:
                        niter += 1
                        if self.max_iter is not None and niter > self.max_iter:
                            break

                        # delayed processing for sentence-based proc.
                        proc_words = []
                        proc_pos = []
                        proc_tags = []
                        for i in range(len(words)):
                            word = words[i]
                            pos = poses[i]
                            tag = tags[i]
                            if self.processing_word is not None:
                                word = self.processing_word(words, i)
                            if self.processing_pos is not None:
                                pos = self.processing_pos(poses, i)
                            if self.processing_tag is not None:
                                tag = self.processing_tag(tags, i)

                            proc_words += [word]
                            proc_pos += [pos]
                            proc_tags += [tag]

                        if self.processing_lexicon is not None:
                            lexicon_vecs = self.processing_lexicon(words)
                            yield proc_words, proc_pos, proc_tags, lexicon_vecs

                        words, poses, tags = [], [], []
                else:
                    ls = line.split()
                    word, tag = ls[0], ls[-1]
                    words += [word]
                    tags += [tag]
                    pos = ls[1]
                    poses += [pos]

    def __len__(self):
        """Iterates once over the corpus to set and store length"""
        if self.length is None:
            self.length = 0
            for _ in self:
                self.length += 1

        return self.length


def load_vocab(filename):
    """Loads vocab from a file

    Args:
        filename: (string) the format of the file must be one word per line.

    Returns:
        d: dict[word] = index

    """
    try:
        print("Loading vocab_file {}...".format(filename))
        d = dict()
        with open(filename, 'rt', encoding='utf8') as f:
            for idx, word in enumerate(f):
                word = word.strip()
                d[word] = idx

    except IOError:
        raise MyIOError(filename)

    print("- done. {} tokens".format(len(d)))

    return d


def get_processing_word(vocab_words=None,
                        vocab_chars=None,
                        lowercase=False,
                        chars=False,
                        allow_unk=True,
                        tag_proc=False):
    """
    단어 리스트와 현재 단어의 인덱스를 입력으로 받고,
    현재 단어를 중심으로 한 n-gram 리스트를 출력하는 함수를 리턴함.
    개별 식별자 변환은 vocab_words와 vocab_ngram이 주어졌을 때 가능함.

    Return lambda function that transform a word (string) into list,
    or tuple of (list, id) of int corresponding to the ids of the word and
    its corresponding characters.

    Args:
        vocab: dict[word] = idx

    Returns:
        f("cat") = ([12, 4, 32], 12345)
                 = (list of char ids, word id)

    """

    def f(words, index):
        return_values = []

        word = words[index]
        # 0. get chars of words
        if vocab_chars is not None and chars is True:
            char_ids = []
            for char in word:
                # ignore chars out of vocabulary
                if char in vocab_chars:
                    char_ids += [vocab_chars[char]]

            return_values.append(char_ids)

        if tag_proc is not True:
            # 1. preprocess word
            if lowercase:
                word = word.lower()

        # 2. get id of word
        if vocab_words is not None:
            if word in vocab_words:
                word = vocab_words[word]
            else:
                if allow_unk:
                    word = vocab_words[UNK]
                else:
                    raise Exception("Unknown key(%s) is not allowed. Check that your vocab (tags?) is correct" % word)
            return_values.append(word)
        else:
            return_values.append(word)

        # 3. return tuple char ids, word id
        if len(return_values) == 1:
            return return_values[0]

        return tuple(return_values)

    return f


def _pad_sequences(sequences, pad_tok, max_length):
    """
    Args:
        sequences: a generator of list or tuple
        pad_tok: the char to pad with

    Returns:
        a list of list where each sublist has same length
    """
    sequence_padded, sequence_length = [], []

    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_length] + [pad_tok] * max(max_length - len(seq), 0)
        sequence_padded += [seq_]
        sequence_length += [min(len(seq), max_length)]

    return sequence_padded, sequence_length


def pad_sequences(sequences, pad_tok, nlevels=1, max_len=0):
    """
    Args:
        sequences: a generator of list or tuple
        pad_tok: the char to pad with
        nlevels: "depth" of padding, for the case where we have characters ids

    Returns:
        a list of list where each sublist has same length

    """
    if nlevels == 1:
        if max_len > 0:
            max_length = max_len
        else:
            max_length = max(map(lambda x: len(x), sequences))
        sequence_padded, sequence_length = _pad_sequences(sequences,
                                                          pad_tok, max_length)

    elif nlevels == 2:
        if max_len > 0:
            max_length_word = max_len
        else:
            max_length_word = max([max(map(lambda x: len(x), seq)) for seq in sequences])

        sequence_padded, sequence_length = [], []
        for seq in sequences:
            # all words are same length now
            sp, sl = _pad_sequences(seq, pad_tok, max_length_word)
            sequence_padded += [sp]
            sequence_length += [sl]

        max_length_sentence = max(map(lambda x: len(x), sequences))
        sequence_padded, _ = _pad_sequences(sequence_padded,
                                            [pad_tok] * max_length_word, max_length_sentence)
        sequence_length, _ = _pad_sequences(sequence_length, 0,
                                            max_length_sentence)

    return sequence_padded, sequence_length


def minibatches(data, minibatch_size):
    """
    Args:
        data: generator of (sentence, tags) tuples
        minibatch_size: (int)

    Yields:
        list of tuples

    """
    x1_batch, x2_batch, y_batch, l_batch = [], [], [], []
    for (x1, x2, y, l) in data:
        if len(x1_batch) == minibatch_size:
            yield x1_batch, x2_batch, y_batch, l_batch
            x1_batch, x2_batch, y_batch, l_batch = [], [], [], []

        if type(x1[0]) == tuple:
            x1 = zip(*x1)
        x1_batch += [x1]
        x2_batch += [x2]
        y_batch += [y]
        l_batch += [l]

    if len(x1_batch) != 0:
        yield x1_batch, x2_batch, y_batch, l_batch


def loading_w2v(w2v_path):
    """

    :param w2v_path:
    :return:
    """
    word_index_dict = {}
    word_vectors = []

    with open(w2v_path, encoding='utf-8') as fin:

        for line in fin:
            line = line.replace('\n', '')
            line = line.replace('\t', '')
            line = line.replace('\r', '')
            tokens = line.split()
            ndims = 0
            if len(tokens) == 2:
                ndims = int(tokens[1])
                word_index_dict[UNK] = len(word_index_dict)  # for UNKNOWN : index = 1
                word_vectors.append(np.random.randn(ndims, ))  # for UNKNOWN : random vector
                continue
            word_index_dict[tokens[0]] = len(word_index_dict)  # 단어 저장...
            vector = np.array([float(tokens[i]) for i in range(1, len(tokens))])
            word_vectors.append(vector)  # 단어벡터 저장...

        word_vectors = np.array(word_vectors, dtype=np.float32)
    return word_index_dict, word_vectors