import json

stop_words = {
    "انتهای": 7005,
    "پیام": 7137,
    "آن": 7142,
    "یک": 7269,
    "نیز": 8024,
    "وی": 8255,
    "کرد": 8311,
    "هزار": 8418,
    "تا": 9009,
    "بر": 9173,
    "شده": 10208,
    "است": 11530,
    "است": 11826,
    "برای": 13604,
    "را": 24719,
    "که": 33334,
    "با": 34228,
    "این": 38162,
    "از": 49211,
    "به": 64682,
    "در": 83032,
    "و": 106082,
    "ها": "",
    "تر": "",
    "ترین": "",
    "بی": "",

}

char_translate = {
    "ْ": "",
    "ٌ": "",
    "ٍ": "",
    "ً": "",
    "ُ": "",
    "ِ": "",
    "َ": "",
    "ّ": "",
    "ٓ": "",
    "ٰ": "",
    "ٔ": "",
    "ؤ": "و",
    "ئ": "ی",
    "ي": "ی",
    "إ": "ا",
    "أ": "ا",
    "آ": "ا",
    "ة": "",
    "ك": "ک",
}

punctuations = [
    "]",
    "[",
    "}",
    "{",
    "؛",
    ":",
    "«",
    "»",
    ">",
    "<",
    "؟",
    "!",
    "٬",
    "﷼",
    "٪",
    "×",
    "،",
    "*",
    ")",
    "(",
    "-",
    "ـ",
    "-",
    "=",
    "+",
    "|",
    "`",
    "~",
    ".",
    ".",
    "»",
    "«"
]

suffixes = {
    "ها": "ها",
    "های": "ها",
    "‌ها": "ها",
    "‌های": "ها",
    "ات": "جمع",
    "‌تر": "جمع",
    "ترین": "جمع",
    "‌ترین": "جمع",
    "ام": "جمع",
    "شان": "جمع",
    "مان": "جمع",
    "تان": "جمع",
    "ان": "جمع",
}


def remove_stop_words(tokens):
    for token in stop_words:
        if token in tokens:
            tokens.pop()


def remove_suffix(word:str):
    with open('utils/dataset/exceptions.json') as f:
        exception_words = json.load(f)
        for suffix in suffixes:
            if word.endswith(suffix) and word not in exception_words:
                return word[:-len(suffix)].strip()
        return word



def remove_prefix(doc):
    prefix = ['بی ', ' می ', ' نمی ']
    prefix2 = ['بی', ' می', ' نمی']
    for char in prefix:
        doc = doc.replace(char, '')
    for char in prefix2:
        char += "\u200c"
        doc = doc.replace(char, '')
    return doc

def pro_words(text):
    #جمع مکسر
    with open('utils/dataset/Arabian.json') as f:
        words=json.load(f)
        for word in words:
            text = text.replace(word, words[word])
    return text


def char_normalizer(doc: str):
    for char in char_translate.keys():
        doc = doc.replace(char, char_translate[char])
    return doc


def remove_punc(docs):
    for punc in punctuations:
        doc = docs.replace(punc, ' ')
    return doc


def separate_words(word):
    if "\u200c" in word:
        return word.split("\u200c")
    else:
        return [word]


def clean_word(word):
    return [remove_suffix(w) for w in separate_words(word)]


def clean_text(text):
    text=char_normalizer(text)
    text=remove_punc(text)
    text=pro_words(text)
    text=remove_prefix(text)
    return text



