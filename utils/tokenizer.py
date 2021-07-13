import csv
import openpyxl
from pathlib import Path
import joblib
from utils.normalizer import clean_text, clean_word


def tokenize_doc(text):
    tokens = {}
    text = clean_text(text)
    words = text.split()
    for word in words:
        if 'http' in word:
            continue
        word_list = clean_word(word)
        for token in word_list:
            if token in tokens:
                tokens[token] += 1
            else:
                tokens[token] = 1
    return tokens


def find_stop_words(tokens, treshhold):
    sorted_ts = {k: v for k, v in sorted(tokens.items(), key=lambda item: item[1])}
    for t in sorted_ts:
        if treshhold == 0:
            break
        treshhold -= 1


def tokenize_documents(documents):
    tokens = {}
    for doc_id, text in enumerate(documents, 1):
        doc_tokens = tokenize_doc(text)
        for token in doc_tokens:
            if token in tokens:
                tokens[token].update({doc_id: doc_tokens[token]})
            else:
                tokens[token] = {doc_id: doc_tokens[token]}
    # # if we need counts
    ls = {token: sum(tokens[token].values()) for token in tokens.keys()}
    find_stop_words(ls, 20)
    return {token: list(tokens[token].keys()) for token in tokens.keys()}
    # # else
    # return tokens


class Tokenizer:
    def __init__(self, data_set, post_index_path=None, update_post=False):
        self.data_set = data_set
        self.post_index = post_index_path
        self.urls = []
        post_index_file = Path('./', post_index_path)
        if post_index_file.is_file() and not update_post:
            self.tokens = joblib.load(post_index_path)
            self.urls=joblib.load("url.pkl")
        else:
            update_post = True
        if update_post:
            documents = self.get_documents()
            self.tokenize(documents)
            joblib.dump(self.tokens, post_index_path)
            joblib.dump(self.urls,"url.pkl")

    def tokenize(self, docs):
        self.tokens = tokenize_documents(docs)

    def get_documents(self):
        filename = self.data_set
        xlsx_file = Path('utils/dataset', filename)
        wb_obj = openpyxl.load_workbook(xlsx_file)
        sheet = wb_obj.active

        documents = []
        for row in sheet.iter_rows(2, sheet.max_row):
            documents.append(row[1].value)
            self.urls.append(row[2].value)
        return documents


