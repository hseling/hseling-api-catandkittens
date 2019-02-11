from error_search.highlighter import HTMLStyle
from error_search.search import Searcher

def process_text(tree, model):
    """
    Обработка входного текста - поиск ошибок
    :param text: входной текст (строка)
    :return: строка, где ошибочные слова окружены соответствующими html-тегами
    """
    if not tree:
        raise Exception("Empty tree")

    searcher = Searcher()
    if not searcher:
        raise Exception("Empty searcher")
    style = HTMLStyle()
    check = searcher.check_all(tree, model)

    sents = []
    for s, sent in enumerate(tree):
        if sent[-1]['misc'] and sent[-1]['misc']['SpacesAfter'] and '\\n' in sent[-1]['misc']['SpacesAfter']:
            s = [i for i in sent.metadata['text'].split()]
            s.append('\n')
            sents.append(s)
        else:
            sents.append([i for i in sent.metadata['text'].split()])

    out_t = []
    for i in range(len(sents)):
        for j in range(len(sents[i])):
            if (sents[i][j], i, j) in check.keys():
                word = str(sents[i][j])
                out_t.append(style.color_scheme[check[(word, i, j)][0]].format(word))
            else:
                out_t.append(sents[i][j])

    string = ' '.join(out_t)
    return string
