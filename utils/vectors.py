import math


def cal_doc_tf(number):
    return 1 + math.log10(number)


def cal_idf(nt, N):
    return math.log(float(N) / nt)


def vectorize_doc(tokens):
    'cal tf of each token in document'
    for token in tokens:
        tokens[token] = {"occur": tokens[token], "tf": cal_doc_tf(tokens[token])}
    return tokens


def vectorizing_docs(tokens, number_of_docs):
    for token in tokens:
        docs = tokens[token]
        idf = cal_idf(len(docs.keys()), number_of_docs)

        docs = {doc_id: {"occur": occur_num, "tf_idf": cal_doc_tf(occur_num) * idf} for doc_id, occur_num in
                docs}  # cal tf for docs

        tokens[token] = docs

    return token

