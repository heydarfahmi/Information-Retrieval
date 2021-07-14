import math
import numpy


def cal_doc_tf(number):
    return 1 + math.log10(number)


def cal_idf(nt, N):
    return math.log(float(N) / nt)


def normalize_vector(array):
    vector = numpy.asarray(array, dtype=numpy.float64).reshape(len(array), 1)
    return vector / numpy.linalg.norm(vector)


def make_vector(tokens, arg="tf"):
    if arg == "tf":
        array = []
        for token in tokens:
            array.append(tokens[token]['tf'])
        return normalize_vector(array)


def make_docs_vector(query_tokens, N, all_tokens, champion_list={}):
    score_matrix = numpy.zeros((N + 1, len(query_tokens)), dtype=numpy.float64)
    for column_id, token in enumerate(query_tokens):
        tf_idf_per_doc = all_tokens.get(token, {})
        for doc in tf_idf_per_doc:
            if champion_list != {}:
                if doc not in champion_list[token]:
                    continue
            score_matrix[doc][column_id] = tf_idf_per_doc[doc]['tf_idf']
    return score_matrix


def cal_scores(matrix_score, query_vector):
    return numpy.dot(matrix_score, query_vector)


def vectorize_doc(tokens):
    'cal tf of each token in document'
    for token in tokens:
        tokens[token] = {"occur": tokens[token], "tf": cal_doc_tf(tokens[token])}
    return tokens


def vectorizing_docs(tokens, number_of_docs, docs_norms):
    for token in tokens:
        docs = tokens[token]
        idf = cal_idf(len(docs.keys()), number_of_docs)
        docs = {doc_id: {"occur": occur_num, "tf_idf": cal_doc_tf(occur_num) * idf} \
                for doc_id, occur_num in docs.items()}  # cal tf for docs
        for doc_id in docs.keys():
            docs_norms[doc_id] += (docs[doc_id]['tf_idf'] ** 2)

        tokens[token] = docs

    for token in tokens:
        docs = tokens[token]
        for doc_id in docs:
            tf_idf = docs[doc_id]['tf_idf'] / math.sqrt(docs_norms[doc_id])
            docs.update({doc_id: {"occur": docs[doc_id]['occur'], "tf_idf": tf_idf}})
        tokens[token] = docs

    return tokens
