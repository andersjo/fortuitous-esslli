from keras.preprocessing import sequence
import numpy as np

def pad_sentences(sentences, max_sentence_len, pad_symbol_id):
    """
    pad sentences all to same length
    """
    return sequence.pad_sequences(sentences, maxlen=max_sentence_len, value=pad_symbol_id)

def pad_words(tensor_words, max_word_len, pad_symbol_id, max_sent_len=None):
    """
    pad character list all to same word length
    """
    padded = []
    for words in tensor_words:
        if max_sent_len:
            words = [[[0]]*(max_sent_len-len(words))+ words][0] #prepending empty words
        padded.append(sequence.pad_sequences(words, maxlen=max_word_len, value=pad_symbol_id))
    return np.array(padded)

def load_embeddings_file(file_name, sep=" ",lower=False):
    """
    load embeddings file
    returns dictionary with word -> vec
    and size of embeddings space
    """
    emb={}
    for line in open(file_name):
        fields = line.split(sep)
        vec = np.asarray(fields[1:], dtype='float32')
        word = fields[0]
        if lower:
            word = word.lower()
        emb[word] = vec

    print("loaded pre-trained embeddings (word->emb_vec) size: {}".format(len(emb.keys())))
    return emb, len(emb[word])
