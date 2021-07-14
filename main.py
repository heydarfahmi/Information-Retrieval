from utils.tokenizer import Tokenizer, tokenize_doc
from utils.sort import k_max
from utils.vectors import (
    vectorize_doc,
    make_vector,
    make_docs_vector,
    cal_scores)

t = Tokenizer('IR_Spring2021_ph12_7k.xlsx', 'test.pkl', True, True)


def get_query_vector(query):
    tokens = tokenize_doc(query)
    tokens = vectorize_doc(tokens)
    return make_vector(tokens)


def get_query(query):
    tokens = tokenize_doc(query)
    if len(tokens.keys()) == 1:
        term = list(tokens.keys())[0]
        print(term)
        if term in t.tokens.keys():
            return {d: t.urls[d - 1] for d in t.tokens[term]}
        else:
            return False
    query_vector = get_query_vector(query)
    print(tokens)
    print(query_vector)
    docs_matrix = make_docs_vector(tokens, t.N, t.tokens)
    scores = cal_scores(docs_matrix, query_vector)
    print(scores)
    best = k_max(list(scores), 10, 0)
    url_best = {doc_ids: t.urls[doc_ids - 1] for doc_ids in best}
    if len(url_best):
        return url_best
    return False


if __name__ == "__main__":
    print("input query")
    query = input()
    result = get_query(query)
    if result is False:
        print("NO DOC FOUND")
    else:
        print(result)
