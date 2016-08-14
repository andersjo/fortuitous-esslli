import codecs

def load_embeddings_file(file_name, sep=" ",lower=False):
    """
    load embeddings file
    """
    emb={}
    for line in codecs.open(file_name,encoding="utf-8"):
        fields = line.split(sep)
        vec = [float(x) for x in fields[1:]]
        word = fields[0]
        if lower:
            word = word.lower()
        emb[word] = vec

    print("loaded pre-trained embeddings (word->emb_vec) size: {} (lower: {})".format(len(emb.keys()), lower))
    return emb, len(emb[word])

def read_conll_file(file_name):
    """
    read in conll file
    word1    tag1
    ...      ...
    wordN    tagN

    Sentences MUST be separated by newlines!

    :param file_name: file to read in
    :return: generator of instances ((list of  words, list of tags) pairs)

    """
    current_words = []
    current_tags = []
    
    for idx, line in enumerate(codecs.open(file_name, encoding='utf-8')):
        line = line.strip()

        if line:
            if len(line.split("\t")) != 2:
                if len(line.split("\t")) == 1: # emtpy words in gimpel
                    print("issue in line number: ", idx, line)
                    word = "|"
                    tag = line.split("\t")[0]
                else:
                    print("erroneous line: {} (line number: {}) ".format(line, i))
                    exit()
            else:
                word, tag = line.split('\t')
            current_words.append(word)
            current_tags.append(tag)

        else:
            yield (current_words, current_tags)
            current_words = []
            current_tags = []

        
    # check for last one
    if current_tags != []:
        yield (current_words, current_tags)
            
    
if __name__=="__main__":
    allsents=[]
    unique_tokens=set()
    for words, tags in read_conll_file("/Users/bplank/corpora/pos/data/twpos/oct27-dev.upos"):
        allsents.append(words)
        unique_tokens.update(words)
    #assert(len(allsents)==1000)
    #assert(len(unique_tokens)==5432)

