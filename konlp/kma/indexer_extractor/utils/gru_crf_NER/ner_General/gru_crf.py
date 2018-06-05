import tensorflow as tf

class GRUCRF(object):
    def __init__(self, args, encoder_symbol_dic, decoder_symbol_dic, feature_size=1040,
                 scope_name="BidirectionalRNNCRF", sylla_embedding = []):
        self.args = args
        self.sylla_embeddings = sylla_embedding
        self.num_encoder_symbols = len(encoder_symbol_dic)
        self.num_decoder_symbols = len(decoder_symbol_dic)
        self.load_flag = False
        self.feature_size = feature_size
        with tf.variable_scope(scope_name):
            with tf.name_scope('placeholder_inputs'):
                self.inputs = tf.placeholder(tf.int32, [None, self.args.max_length], "inputs")
                self.sequence_length = tf.placeholder(tf.int32, [None])
            with tf.name_scope('placeholder_outputs'):
                self.outputs = tf.placeholder(tf.int32, [None, self.args.max_length], "outputs")
            with tf.name_scope('placeholder_feature_inputs'):
                self.pl_hasDic = tf.placeholder(tf.float32, [None, self.args.max_length, self.feature_size],"hasDic")
            with tf.name_scope('placeholder_keep_prob'):
                self.keep_prob = tf.placeholder(tf.float32, [], "keep_prob")
            with tf.name_scope("transition"):
                self.save_transition = tf.get_variable("save_transition",
                                                       [self.num_decoder_symbols, self.num_decoder_symbols],
                                                       initializer=tf.random_normal_initializer(stddev=0.1))
                self.transition = tf.placeholder(tf.float32, [None, None], "transition_placeholder")
                self.update_transition = self.save_transition.assign(self.transition)

            # self.embeddings = tf.get_variable("embedding", [self.num_encoder_symbols, self.args.embedding_size], initializer=tf.random_normal_initializer(stddev=0.1))
            self.embeddings = tf.get_variable("embedding", [self.num_encoder_symbols, self.args.embedding_size], initializer=tf.constant_initializer(self.sylla_embeddings))

            encoder_embedding_inputs = tf.nn.embedding_lookup(self.embeddings, self.inputs)
                # batch * n_step *  * embedding

            #batch * n_step * embedding
            encoder_embedding_inputs = tf.concat([encoder_embedding_inputs, self.pl_hasDic],2)
            # batch * n_step * (embedding+feature)
            encoder_embedding_inputs = [tf.reshape(i,(-1, self.args.embedding_size+self.feature_size)) for i in tf.split(encoder_embedding_inputs, self.args.max_length, 1)]

            # step * batch * (embedding + feature)
            with tf.variable_scope("rnn") as scope:
                if self.args.cell_mode == "LSTM":
                    encoder_fw_cell = tf.contrib.rnn.LSTMCell(self.args.hidden_size)
                    encoder_bw_cell = tf.contrib.rnn.LSTMCell(self.args.hidden_size)
                elif self.args.cell_mode == "GRU":
                    encoder_fw_cell = tf.contrib.rnn.GRUCell(self.args.hidden_size)
                    encoder_bw_cell = tf.contrib.rnn.GRUCell(self.args.hidden_size)
                else:
                    encoder_fw_cell = tf.contrib.rnn.BasicRNNCell(self.args.hidden_size)
                    encoder_bw_cell = tf.contrib.rnn.BasicRNNCell(self.args.hidden_size)
                encoder_fw_cell = tf.contrib.rnn.DropoutWrapper(encoder_fw_cell, input_keep_prob=self.keep_prob,output_keep_prob=self.keep_prob)
                encoder_bw_cell = tf.contrib.rnn.DropoutWrapper(encoder_bw_cell, input_keep_prob=self.keep_prob,output_keep_prob=self.keep_prob)

                if self.args.num_layers > 1:
                    encoder_fw_cell = tf.contrib.rnn.MultiRNNCell([encoder_fw_cell] * self.args.num_layers,
                                                               state_is_tuple=True)
                    encoder_bw_cell = tf.contrib.rnn.MultiRNNCell([encoder_bw_cell] * self.args.num_layers,
                                                               state_is_tuple=True)

                encoder_outputs, _ ,_= tf.contrib.rnn.static_bidirectional_rnn(cell_fw=encoder_fw_cell,
                                                                   cell_bw=encoder_bw_cell,
                                                                   inputs=encoder_embedding_inputs,
                                                                   dtype=tf.float32,
                                                                   sequence_length=self.sequence_length,
                                                                   scope=scope)

                encoder_outputs = tf.transpose(encoder_outputs, [1, 0, 2])
                # encoder_state = tf.concat(encoder_state, 1)
            with tf.variable_scope("crf") as scope:
                crf_weights = tf.get_variable("crf_weights", [self.args.hidden_size * 2, self.num_decoder_symbols])
                matricized_x_t = tf.reshape(encoder_outputs, [-1, self.args.hidden_size * 2])
                matricized_unary_scores = tf.matmul(matricized_x_t, crf_weights)
                self.unary_scores = tf.reshape(matricized_unary_scores,[self.args.batch_size, self.args.max_length, self.num_decoder_symbols])

                log_likelihood, self.transition_params = tf.contrib.crf.crf_log_likelihood(self.unary_scores,
                                                                                           self.outputs,
                                                                                           self.sequence_length)
                self.loss = tf.div(tf.reduce_mean(-log_likelihood), self.args.batch_size)
                self.train_op = tf.train.AdamOptimizer(self.args.learning_rate).minimize(self.loss)
                # self.train_op = tf.train.GradientDescentOptimizer(self.args.learning_rate).minimize(self.loss)
                # self.train_op = tf.train.AdadeltaOptimizer(self.args.learning_rate).minimize(self.loss)
                self.saver = tf.train.Saver(
                                            max_to_keep=10)

    def save_model(self, session, path):
        checkpoint_path = path
        print("Saving model, %s" % (checkpoint_path))
        self.saver.save(session, checkpoint_path)

    def load_model(self, session, path):
        ckpt = tf.train.get_checkpoint_state(path)
        if ckpt:
            file_name = ckpt.model_checkpoint_path + ".meta"

        if ckpt and tf.gfile.Exists(file_name):
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            self.saver.restore(session, ckpt.model_checkpoint_path)
        else:
            print("Created model with fresh parameters.")
            session.run(tf.global_variables_initializer())

    def train_step(self, session, train_x, train_hasDic, train_y, sequence_length, keep_prob):

        input_feed = {
            self.inputs: train_x,
            self.pl_hasDic:train_hasDic,
            self.keep_prob:keep_prob,
            self.outputs: train_y,
            self.sequence_length: sequence_length}

        if not self.load_flag:
            output_feed = [
                self.unary_scores,
                self.save_transition,
                self.train_op,
                self.loss]
            self.load_flag = True
            print("Success Transition Load")
            tf_unary_scores, tf_transition_params, _, loss = session.run(output_feed, feed_dict=input_feed)
            #             tf_transition_params = self.save_transition
        else:
            output_feed = [
                self.unary_scores,
                self.transition_params,
                self.train_op,
                self.loss]
            tf_unary_scores, tf_transition_params, _, loss = session.run(output_feed, feed_dict=input_feed)
        session.run(self.update_transition, feed_dict={self.transition: tf_transition_params})

        return loss

    def predict_step(self, session, test_x, test_hasDic, sequence_length, keep_prob):
        output_feed = [self.unary_scores, self.save_transition]
        input_feed = {
            self.inputs: test_x,
            self.pl_hasDic: test_hasDic,
            self.keep_prob:keep_prob,
            self.sequence_length: sequence_length}
        tf_unary_scores, transition = session.run(output_feed, feed_dict=input_feed)

        resultList = []
        for tf_unary_scores_, sequence_length_ in zip(tf_unary_scores, sequence_length):
            tf_unary_scores_ = tf_unary_scores_[:sequence_length_]
            viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(tf_unary_scores_, transition)
            resultList.append(viterbi_sequence)

        return resultList

    def get_batch(self, batch_data, max_length):
        symbol = {"PAD_ID": 0}

        batch_train_x, batch_train_y, batch_weights = [], [], []

        batch_sequence_length = []

        for idx in range(len(batch_data)):
            x, y, sequence_length = batch_data[idx]
            batch_sequence_length.append(sequence_length)

            x_pad = [symbol["PAD_ID"]] * (max_length - len(x))
            batch_train_x.append(list(x + x_pad))
            y_pad = [symbol["PAD_ID"]] * (max_length - len(y))
            batch_train_y.append(list(y + y_pad))
            weight = list(([1.0] * len(x)) + [0.0] * (max_length - len(x)))
            batch_weights.append(weight)

        return batch_train_x, batch_train_y, batch_weights, batch_sequence_length

    # def save_model(self, session, path):
    #     print(path)
    #     checkpoint_path = path
    #     print("Saving model, %s" % (checkpoint_path))
    #     self.saver.save(session, checkpoint_path)
    #
    # def load_model(self, session, path):
    #     ckpt = tf.train.get_checkpoint_state(path)
    #     if ckpt:
    #         file_name = ckpt.model_checkpoint_path + ".meta"
    #
    #     if ckpt and tf.gfile.Exists(file_name):
    #         print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
    #         self.saver.restore(session, ckpt.model_checkpoint_path)
    #     else:
    #         print("Created model with fresh parameters.")
    #         session.run(tf.global_variables_initializer())

    def get_batch_index_list(self, data):
        total_batch = int(len(data) / self.args.batch_size)
        index_list = []
        for i in range(total_batch):
            if i * self.args.batch_size < len(data):
                index_list.append((0 + i * self.args.batch_size, self.args.batch_size + i * self.args.batch_size))
            else:
                index_list.append((0 + i * self.args.batch_size, len(data)))
        return index_list

if __name__ == "__main__":

    tf.app.flags.DEFINE_integer("hidden_size", 512, "hidden_size")
    tf.app.flags.DEFINE_integer("embedding_size", 50, "embedding_size")
    tf.app.flags.DEFINE_integer("max_length", 100, "max_input_length")
    tf.app.flags.DEFINE_integer("batch_size", 30, "batch_size")
    tf.app.flags.DEFINE_integer("num_layers", 1, "num_layers")
    tf.app.flags.DEFINE_float("learning_rate", 0.01, "learning_rate")
    tf.app.flags.DEFINE_float("dropout", 0.7, "dropout")
    tf.app.flags.DEFINE_string("cell_mode", "GRU", "cell_mode")
    tf.app.flags.DEFINE_bool("test", False, "test")

    word2idx = {"<PADDING>": 0, "<START>": 1, "<END>": 2, "<UNK>": 3}
    decode_word2idx = {"<PADDING>": 0, "<START>": 1, "<END>": 2, "<UNK>": 3}

    for i in range(46):
        word2idx[i] = i
        decode_word2idx[i] = i
    args = tf.app.flags.FLAGS

    model = GRUCRF(args, word2idx, decode_word2idx)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))

    data_set = []
    print("####")

    inputs = []
    outputs = []
    sequence_length = []
    for _ in range(10):
        inputs.append([5, 4, 3, 3, 4, 3, 4, 5, 7, 8, 5, 4, 3, 3, 4, 3, 4, 5, 7, 8])
        outputs.append([4, 3, 2, 2, 3, 2, 3, 4, 6, 7, 4, 3, 2, 2, 3, 2, 3, 4, 6, 7])
        sequence_length.append(20)
        if len(sequence_length)==args.batch_size:
            data_set.append((inputs, outputs, sequence_length))
            inputs = []
            outputs = []
            sequence_length = []

    path = "../model"
    model.load_model(sess, path)

    for epoch in range(100):
        for batch in range(len(data_set)):
            (inputs, outputs, sequence_length) = data_set[batch]
            print(len(inputs[0]))
            print(len(outputs[0]))
            print(sequence_length[0])
            result = model.train_step(sess, inputs, outputs, sequence_length)
            print(result)

            model.save_model(sess, path, epoch, batch)

    inputs = []
    outputs = []
    sequence_length = []
    for _ in range(1):
        inputs.append([5, 4, 3, 3, 4, 3, 4, 5, 7, 8, 5, 4, 3, 3, 4, 3, 4, 5, 7, 8])
        outputs.append([4, 3, 2, 2, 3, 2, 3, 4, 6, 7, 4, 3, 2, 2, 3, 2, 3, 4, 6, 7])
        sequence_length.append(20)
    result_list = model.predict_step(sess,inputs,sequence_length)
    print (result_list)
