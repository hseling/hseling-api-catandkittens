from collections import defaultdict
from gensim.models import Word2Vec
import logging
from alphabet_detector import AlphabetDetector


MORE_LESS = ['более', 'менее']
STATISTICS = "maxs"
MODEL = 'Linguistics/LinguisticsModel'
wv_model = Word2Vec.load(MODEL)

class Searcher:
    """
    Поиск ошибок. Переработан так, чтобы удобнее было перезаписывать текст с найденными ошибками для вывода пользователю
    """
    def __init__(self):
        self.found = defaultdict(list)
        self.flag_i_vs_we = ''
        self.found_word = defaultdict(list)

    def find_genitives(self, gen_chain, word, s, i, threshold=6):
        if word['feats'] and 'Case' in word['feats'].keys() and word['feats']['Case'] == 'Gen':
            gen_chain.append((word['form'], s, i))
        else:
            if len(gen_chain) >= int(threshold):
                self.found['genitives'].append(gen_chain)
                for gen in gen_chain:
                    self.found_word[gen].append('genitives')
            gen_chain = []
        return gen_chain

    def find_wrong_comparativ(self, sent, word, i, s):
        if i + 1 < len(sent):
            next = sent[i + 1]
            if word['form'] in MORE_LESS and 'comp' in next['feats']:
                self.found['comparatives'].append((word['form'], next['form'], s, i))
                self.found_word[(word['form'], s, i)].append('comparatives')

    # !
    def find_wrong_coordinate_NPs(self, sent, i, s, word, model):
        if i + 1 < len(sent):
            if word['form'] == 'и':
                t = i
                pair = []
                while (sent[t]['feats'] and 'S' not in sent[t]['feats']) and (
                        sent[t]['feats'] and 'V' not in sent[t]['feats']) and t > 0:
                    t -= 1
                if sent[t]['feats'] and 'S' in sent[t]['feats']:
                    pair.append(sent[t]['form'])
                t = i
                while (sent[t]['feats'] and 'S' not in sent[t]['feats']) and (
                        sent[t]['feats'] and 'V' not in sent[t]['feats']) and t < len(sent):
                    t += 1
                if sent[t]['feats'] and 'S' in sent[t]['feats']:
                    pair.append(sent[t]['form'])
                if len(pair) > 1:
                    if pair[0] in model.wv.vocab and pair[1] in model.wv.vocab:
                        self.found['coordinate_NPs'].append(pair + [s, i, model.similarity(pair[0], pair[1])])
                    else:
                        self.found['coordinate_NPs'].append(pair + [s, i, float('-inf')])
                    self.found_word[(pair[0], s, i)].append('coordinate_NPs')
                    self.found_word[(pair[1], s, i + 1)].append('coordinate_NPs')

    def not_in_vocabulary(self, ad, word, i, model, s):
        if word['form'].isalpha() and ad.only_alphabet_chars(word['form'], "CYRILLIC") and word[
            'form'].lower() not in model.wv.vocab:
            self.found['not in vocabulary'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('not in vocabulary')

    def i_vs_we(self, i, word, s):
        if word['lemma'] == 'Я' and not self.flag_i_vs_we:
            self.flag_i_vs_we = 'i'
            self.found['i vs we'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('i vs we')
        elif (word['lemma'] == 'Я' and self.flag_i_vs_we == 'we') or (
                word['lemma'] == 'МЫ' and self.flag_i_vs_we == 'i'):
            self.found['i vs we'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('i vs we')
        elif word['lemma'] == 'МЫ' and not self.flag_i_vs_we:
            self.flag_i_vs_we = 'we'
            self.found['i vs we'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('i vs we')

    def check_mood(self, sent, i, word, s):
        if word['form'] == 'бы' and i > 0:
            self.found['subjunctive mood'].append((sent[i - 1]['form'], word['form'], s, i))
            self.found_word[(sent[i - 1]['form'], s, i - 1)].append('subjunctive mood')
            self.found_word[(word['form'], s, i)].append('subjunctive mood')
        if word['feats'] and 'Mood' in word['feats'].keys() and word['feats']['Mood'] == 'Imp':
            self.found['imperative mood'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('imperative mood')

    def check_all(self, tree):
        # s - sentence number
        # i - word number
        logging.basicConfig(level=logging.INFO, filename='found.log')
        model = Word2Vec.load(MODEL)
        ad = AlphabetDetector()

        for s, sent in enumerate(tree):
            gen_chain = []

            for i, word in enumerate(sent):
                self.check_mood(sent, i, word, s)
                self.i_vs_we(i, word, s)
                self.not_in_vocabulary(ad, word, i, model, s)
                gen_chain = self.find_genitives(gen_chain, word, s, i)
                self.find_wrong_comparativ(sent, word, i, s)
                self.find_wrong_coordinate_NPs(sent, i, s, word, model)

        for key, value in self.found.items():
            logging.info(key)
            for mistake in value:
                logging.info(mistake)

        return self.found_word