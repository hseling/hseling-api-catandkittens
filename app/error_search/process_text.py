from conllu import parse
from ufal.udpipe import Model, Pipeline
from error_search.highlighter import HTMLStyle
from error_search.search import Searcher

ud_model = Model.load('russian-syntagrus-ud-2.3-181115.udpipe')

pipeline = Pipeline(ud_model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

searcher = Searcher()

style = HTMLStyle()

def process_text(text):
    """
    Обработка входного текста - поиск ошибок
    :param text: входной текст (строка)
    :return: строка, где ошибочные слова окружены соответствующими html-тегами
    """
    out = pipeline.process(text)
    tree = parse(out)
    check = searcher.check_all(tree)

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
