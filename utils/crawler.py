from bs4 import BeautifulSoup
from requests import request


def crawl_isna_page(url):
    r = request('POST', url)
    bs = BeautifulSoup(r.text, 'html.parser')
    img = bs.select('.img-md img')[0].get('src')
    header = bs.select('.first-title')[0].get_text()
    summary = bs.select('.summary')[0].get_text()
    category = bs.select('.fa-folder-o~ .text-meta')[0].get_text().replace(' ', '').replace('\n', '').split('،')
    tags = bs.select('.tags a')
    tags = [tag.get_text() for tag in tags]
    docs = bs.select('.item-text p')[:-1]
    doc_text = '\n \n'.join([doc.get_text() for doc in docs])
    return {
        'doc_text': doc_text,
        'header': header,
        'img': img,
        'summary': summary,
        'category': category,
        'tags': tags
    }


def make_json(lists):
    result = []
    for row in lists:
        dict = crawl_isna_page(row[1])
        full_text = dict['header'] + "\n" + dict['summary'] + "\n" + dict["doc_text"]

        [row[0], full_text]

    return result
