from utils.tokenizer import Tokenizer
from utils.normalizer import clean_word,clean_text
t = Tokenizer('IR_Spring2021_ph12_7k.xlsx', 'test.pkl', False)


def get_query(query):

    print(query)
    query=clean_text(query)
    sep_query=query.split()
    query_words=[]
    for any_word in sep_query:
        words=clean_word(any_word)
        for word in words:
            if word in query_words:
                continue
            query_words.append(word)
    if len(query_words) == 1:
        if query_words[0] in t.tokens.keys():
            return {d: t.urls[d - 1] for d in t.tokens[query_words[0]]}
        else:
            return False
    doc_scores = {}
    for word in query_words:
        if word in t.tokens:
            doc_scores.update({d: doc_scores.get(d, 0)+1 for d in t.tokens[word]})
    doc_scores = dict(sorted(doc_scores.items(), key=lambda item: item[1],reverse=True))
    doc_scores={d:{"score":k,"url":t.urls[d-1]} for d,k in doc_scores.items()}
    if len(doc_scores):
        return doc_scores
    return False


if __name__ == "__main__":
    print("input query")
    query = input()
    result=get_query(query)
    if result is False:
        print("NO DOC FOUND")
    else:
        print(result)