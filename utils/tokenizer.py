import csv
import openpyxl
from pathlib import Path


def tokenize_doc(text):
    tokens = {}
    words = text.split()
    for word in words:
        if 'http' in word:
            continue
        if word in tokens:
            tokens[word] += 1
        else:
            tokens[word] = 1
    return tokens


def tokenize_documents(documents):
    tokens = {}
    for doc_id, text in enumerate(documents, 1):
        doc_tokens = tokenize_doc(text)
        for token in doc_tokens:
            if token in tokens:
                tokens[token].update({doc_id: doc_tokens[token]})
            else:
                tokens[token] = {doc_id: doc_tokens[token]}

    # if we need counts
    # return tokens
    # else
    return {token: list(tokens[token].keys()) for token in tokens.keys()}


class Tokenizer:
    def __init__(self, data_set, post_index=None, update_post=False):
        self.data_set = data_set
        self.post_index = post_index
        if update_post:
            pass
        if post_index is None:
            update_post = True
        if update_post:
            documents = self.get_documents()
            self.tokens = tokenize_documents(documents)

    def tokenize(self):
        pass

    def get_documents(self):
        filename = self.data_set
        xlsx_file = Path('dataset', filename)
        wb_obj = openpyxl.load_workbook(xlsx_file)
        sheet = wb_obj.active

        documents = []
        for row in sheet.iter_rows(2, sheet.max_row):
            documents.append(row[1].value)
        return documents


t = Tokenizer('IR_Spring2021_ph12_7k.xlsx', None)
# t.get_documents()
