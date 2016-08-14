from keras.utils import np_utils

from lib.mio import read_conll_file
from lib.utils import pad_sentences

import os
import sys
import numpy as np

class AbstractTagger(object):
    """
      Main abstract class of a sequence tagger
      implement the build_graph for different architectures
      """
    def __init__(self,seed=None):
        self.w2i = {}  # word to index mapping
        self.t2i = {}  # tag to index mapping
        if seed:
            self.set_seed(seed)

    def set_seed(self, seed):
        self.seed = seed
        np.random.seed(seed)

    def build_graph(self):
        raise "Not implemented: need to specify in subclass"

    def get_num_features(self):
        return len(self.w2i)

    def get_num_tags(self):
        return len(self.t2i)

    def predict(self, input, output=None, batch_size=32):
        # predictions = self.model.predict_classes(self.test_X)
        #  nb: predict_classes only in non-functional api (https://github.com/fchollet/keras/issues/2524)
        probs = self.model.predict(input, batch_size=batch_size)

        if probs.shape[-1] > 1:
            predictions = probs.argmax(axis=-1)
        else:
            predictions = (probs > 0.5).astype('int32')  # binary

        return self.evaluate(predictions, output)

    def evaluate(self, predictions, output):
        i2t = {idx: tag for tag, idx in self.t2i.items()}
        i2w = {v: w for w, v in self.w2i.items()}

        if output:
            if os.path.isdir(output):
                outdir = os.path.dirname(output)
                if not os.path.exists(outdir):
                    os.makedirs(outdir)

            file_pred = output
            sys.stdout = open(file_pred, 'w')

        correct = 0.0
        total = 0.0

        for pred, inst, gold in zip(predictions, self.test_X_in, self.test_Y_in):
            # get only last part (non-padded)
            predicted_unpadded = [i2t[tid]for tid in pred[-len(inst):]]

            input = [i2w[w] for w in inst]
            gold = [i2t[tag] for tag in gold]
            assert (len(predicted_unpadded) == len(gold))
            for word, p, g in zip(input, predicted_unpadded, gold):
                if output:
                    print("{}\t{}\t{}".format(word, g, p))
                if p == g:
                    correct += 1
                total += 1
            if output:
                print("")
                # print(predicted_tags)
        print("correct {} total: {} accuracy: {}".format(correct, total, correct / total), file=sys.stderr)
        ## nb. for Time distributed models with padding, don't use model.evaluate (counts paddings in!)


class SequenceTagger(AbstractTagger):

    def make_data(self, file_name, w2i=None, t2i=None, freeze=False):
        """
        transform data to features (map word to indices, w2i); reserve index 0 for PADDING, 1 for UNK
        map tags to indices (t2i) [in Keras labels need to be integers]
        :freeze: False = test data (do not add new words)
        """
        if not w2i:
            w2i = {"<pad>": 0, "_UNK": 1}
            #t2i = {"<padtag>": 0} # get rid of padtag and use masks!
            t2i = {}

        X = []
        Y = []
        X_org = [] # keep original words for type-constr.
        num_sentences = 0
        num_tokens = 0

        for instance_idx, (words, tags) in enumerate(read_conll_file(file_name)):

            num_sentences += 1
            instance_feats_indices = []  # sequence of word indices
            instance_tags_indices = []  # sequence of tag indices

            for i, (word, tag) in enumerate(zip(words, tags)):
                num_tokens += 1
                # map words and tags to indices
                if word not in w2i:
                    if not freeze:
                        w2i[word] = len(w2i)
                        instance_feats_indices.append(w2i[word])
                    else:
                        # set to UNK
                        instance_feats_indices.append(w2i["_UNK"])
                else:
                    instance_feats_indices.append(w2i[word])

                if not freeze:
                    if tag not in t2i:
                        t2i[tag] = len(t2i) #+1 #start from 1 (reserve 0 for padding!)

                instance_tags_indices.append(t2i.get(tag))

            X.append(instance_feats_indices)
            Y.append(instance_tags_indices)
            X_org.append(words)

        if not freeze: # when reading train data
            i2t = {id: tag for tag, id in t2i.items()}
            print("%s sentences %s tokens" % (num_sentences, num_tokens), file=sys.stderr)
            print("%s features" % len(w2i), file=sys.stderr)

        assert (len(X) == len(Y))  # make sure lengths match
        if not freeze:
            return X, Y, w2i, t2i  # return token/tag indices
        else:
            return X, Y, X_org

    def read_data(self, trainfile, testfile, dev=None, freeze=False):
        """
        reads in CoNLL files, maps tokens and tags to indices, pads sequences
        sets self.train_X, self.train_Y [and same for test_X|Y, and dev_X|Y]
        """
        print(trainfile)
        # convert word 2 indices, labels 2 number
        train_X_in, train_Y_in, self.w2i, self.t2i = self.make_data(trainfile)
        self.test_X_in, self.test_Y_in, self.test_X_org = self.make_data(testfile, w2i=self.w2i, t2i=self.t2i, freeze=True) #keep textX for later
        self.max_sentence_len = max([len(s) for s in train_X_in] + [len(s) for s in self.test_X_in])
        print("max_sentence_len:", self.max_sentence_len, file=sys.stderr)

        # pad sequences
        self.train_X = pad_sentences(train_X_in, self.max_sentence_len, self.w2i["<pad>"])
        train_Y_padded = pad_sentences(train_Y_in, self.max_sentence_len,0)
        self.test_X = pad_sentences(self.test_X_in, self.max_sentence_len, self.w2i["<pad>"])
        test_Y_padded = pad_sentences(self.test_Y_in, self.max_sentence_len, 0)

        nb_classes = len(self.t2i)

        # convert class vectors to one-hot
        self.train_Y = np.array([list(np_utils.to_categorical(seq, nb_classes)) for seq in train_Y_padded])
        self.test_Y = np.array([list(np_utils.to_categorical(seq, nb_classes)) for seq in test_Y_padded])
        if dev:
            dev_X_in, dev_Y_in, dev_X_org = self.make_data(dev, w2i=self.w2i, t2i=self.t2i, freeze=True)
            self.dev_X = pad_sentences(dev_X_in, self.max_sentence_len, self.w2i["<pad>"])
            dev_Y_padded = pad_sentences(dev_Y_in, self.max_sentence_len, 0)
            self.dev_Y = [list(np_utils.to_categorical(seq, nb_classes)) for seq in dev_Y_padded]


    def fit(self, batch_size, epochs, dev=None, callbacks=[]):
        if dev:
            self.model.fit(self.train_X, self.train_Y, batch_size=batch_size,
                           callbacks=callbacks, nb_epoch=epochs,
                           validation_data=(self.dev_X, self.dev_Y))
        else:
            self.model.fit(self.train_X, self.train_Y, batch_size=batch_size,
                           callbacks=callbacks, nb_epoch=epochs)


