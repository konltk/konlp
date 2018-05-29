import tensorflow as tf
from konlp.tag.kguner.lib.data_utils import pad_sequences


class BaseModel(object):
    """Generic class for general methods that are not specific to KGUNER"""

    def __init__(self, config):
        """Defines self.config

        Args:
            config: (Config instance) class with hyper parameters,
                vocab and embeddings

        """
        self.config = config
        self.sess = None
        self.saver = None

    def initialize_session(self):
        """Defines self.sess and initialize the variables"""
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()

    def close_session(self):
        """Closes the session"""
        self.sess.close()


class NERModel(BaseModel):
    """Specialized class of Model for KGUNER"""

    def __init__(self, config):
        super(NERModel, self).__init__(config)
        self.idx_to_tag = {idx: tag for tag, idx in
                           self.config.vocab_tags.items()}

    def get_feed_dict_in_graph(self, words, pos, graph, lexicon_vecs=None, dropout=None):
        """Given some data, pad it and build a feed dictionary

        Args:
            words: list of sentences. A sentence is a list of ids of a list of
                words. A word is a list of ids
            labels: list of ids
            lr: (float) learning rate
            dropout: (float) keep prob

        Returns:
            dict {placeholder: value}

        """

        graph_words = graph.get_tensor_by_name('prefix/word_ids:0')
        graph_pos = graph.get_tensor_by_name('prefix/pos_ids:0')
        graph_chars = graph.get_tensor_by_name('prefix/char_ids:0')
        graph_wordlens = graph.get_tensor_by_name('prefix/word_lengths:0')
        graph_seqlens = graph.get_tensor_by_name('prefix/sequence_lengths:0')
        graph_lexicon = graph.get_tensor_by_name('prefix/lexicon_vectors:0')
        graph_dropout = graph.get_tensor_by_name('prefix/dropout:0')

        # perform padding of the given data
        if self.config.use_chars:
            char_ids, word_ids = zip(*words)
            word_ids, sequence_lengths = pad_sequences(word_ids, 0)
            pos_ids, _ = pad_sequences(pos, 0)
            char_ids, word_lengths = pad_sequences(char_ids, pad_tok=0, nlevels=2)
        else:
            word_ids, sequence_lengths = pad_sequences(words, 0)
            pos_ids, _ = pad_sequences(pos, 0)

        # build feed dictionary
        feed = {
            graph_words: word_ids,
            graph_pos: pos_ids,
            graph_seqlens: sequence_lengths
        }

        if self.config.use_chars:
            feed[graph_chars] = char_ids
            feed[graph_wordlens] = word_lengths

        if self.config.use_lexicons and lexicon_vecs:
            lex_vecs, _ = pad_sequences(lexicon_vecs, 0)
            feed[graph_lexicon] = lex_vecs

        if dropout is not None:
            feed[graph_dropout] = dropout

        return feed, sequence_lengths

    def predict_batch_in_graph(self, words, pos, graph, lexicon_vecs=None):
        """
        Args:
            words: list of sentences

        Returns:
            labels_pred: list of labels for each sentence
            sequence_length

        """

        self.graph_logits = graph.get_tensor_by_name("prefix/proj/Reshape_1:0")
        self.graph_trans_params = graph.get_tensor_by_name("prefix/transitions:0")

        fd, sequence_lengths = self.get_feed_dict_in_graph(words, pos, graph=graph,
                                                           lexicon_vecs=lexicon_vecs, dropout=1.0)

        # get tag scores and transition params of CRF
        viterbi_sequences = []
        logits, trans_params = self.sess.run(
            [self.graph_logits, self.graph_trans_params], feed_dict=fd)

        # iterate over the sentences because no batching in vitervi_decode
        for logit, sequence_length in zip(logits, sequence_lengths):
            logit = logit[:sequence_length]  # keep only the valid steps
            viterbi_seq, viterbi_score = tf.contrib.crf.viterbi_decode(
                logit, trans_params)
            viterbi_sequences += [viterbi_seq]

        return viterbi_sequences